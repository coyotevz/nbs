# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from nbs.models import db
from nbs.models.misc import TimestampMixin
from nbs.models.stock import ProductStock, StockTransaction
from nbs.utils import dq


class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    id = db.Column(db.Integer, primary_key=True)

    #: category description
    description = db.Column(db.Unicode, nullable=False)

    #: suggested markup when calculating the product's price
    suggested_markup = db.Column(db.Numeric(10, 5))

    #: A saleman suggested commission for products of this category.
    suggested_commission = db.Column(db.Numeric(10, 5))

    parent_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    parent = db.relationship('ProductCategory', backref='children',
                             remote_side=[id])

    def get_commission(self):
        """Returns the commission for this category.
        If it's unset, return the value of the base category, if any.
        """
        if self.parent:
            return (self.suggested_commission or
                    self.parent.get_commission())
        return self.suggested_commission

    def get_markup(self):
        """Returns the markup for this category.
        If it's unset, return the value of the base category, if any.
        """
        if self.parent:
            return (self.suggested_markup or
                    self.parent.get_markup())
        return self.suggested_markup

    def get_path(self):
        parent = self
        path = []
        while parent:
            path.append(parent)
            parent = parent.parent
        return reversed(path)

    def get_children_recursively(self):
        """Return all the children from this category, recursively.
        """
        children = set(self.children)
        if not len(children):
            return set()

        for child in self.children:
            children |= child.get_children_recursively()
        return children

    def __repr__(self):
        return "<ProductCategory({0})>".format(
                self.description.encode('utf-8')
        )


class Product(db.Model, TimestampMixin):
    """Product that can be selled and stored"""
    __tablename__ = 'product'

    #: the product is available and can be used on a |purchase|/|sale|
    STATUS_AVAILABLE = u'STATUS_AVAILABLE'

    #: the product is closed, that is, it still exists for references,
    #: but it should no be possible to create |purchase|/|sale| with it
    STATUS_CLOSED = u'STATUS_CLOSED'

    #: the product is suspended, that is, it still exists for future references
    #: but it should not be possible to create a |purchase|/|sale| with it
    #: until back to available status.
    STATUS_SUSPENDED = u'STATUS_SUSPENDED'

    _statuses = {
        STATUS_AVAILABLE: u'Disponible',
        STATUS_CLOSED: u'Cerrado',
        STATUS_SUSPENDED: u'Suspendido',
    }

    TYPE_PERMANENT = u'TYPE_PERMANENT'
    TYPE_ON_REQUEST = u'TYPE_ON_REQUEST'
    TYPE_CONSIGMENT = u'TYPE_CONSIGMENT'

    _product_types = {
        TYPE_PERMANENT: u'Permanente',
        TYPE_ON_REQUEST: u'Bajo Pedido',
        TYPE_CONSIGMENT: u'Consignacion',
    }

    id = db.Column(db.Integer, primary_key=True)

    #: stock keeping unit, for internal identifying the sellable product
    sku = db.Column(db.Unicode(24), index=True, nullable=False, unique=True)

    #: barcode, ussually printted and attached to the package
    barcode = db.Column(db.Unicode(48), unique=True)

    #: full description of sellable product
    description = db.Column(db.Unicode(128), nullable=False)

    #: short description (mostly for Fiscal Ticket)
    short_description = db.Column(db.Unicode(40))

    #: notes for this product
    notes = db.Column(db.UnicodeText)
    
    #: sale price without taxes
    price = db.Column(db.Numeric(10, 2), nullable=False)

    #: Use markup formula to calculate sale price ?
    automatic_price = db.Column(db.Boolean, default=False)

    #: cost of this product
    _cost = db.Column('cost', db.Numeric(10, 2))

    #: Use ProductSupplierInfo.cost to calculate cost
    automatic_cost = db.Column(db.Boolean, default=False)

    #: saleman commission factor (comission factor x sale price) = commission
    commission = db.Column(db.Numeric(10, 5))

    #: unit of the product, kg, l, etc.
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = db.relationship('ProductUnit', backref=db.backref('products',
                                                             lazy='dynamic'))

    #: category this product belong to
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category = db.relationship('ProductCategory',
                               backref=db.backref('products', lazy='dynamic'))

    tax_constant_id = db.Column(db.Integer,
                                db.ForeignKey('tax_constant.id'))
    tax_constant = db.relationship('TaxConstant',
                                   backref=db.backref('products',
                                                      lazy='dynamic'))

    status = db.Column(db.Enum(*_statuses.keys(), name='product_status_enum'),
                       default=STATUS_AVAILABLE)

    product_type = db.Column(db.Enum(*_product_types.keys(),
                             name='product_type_enum'), default=TYPE_PERMANENT)

    #: 'created' field added by TimestampMixin
    #: 'modified' field added by TimestampMixin

    #: PriceComponents for automatic price calculation
    markup_components = db.relationship('PriceComponent',
            backref=db.backref("product_markup", lazy='dynamic'),
            secondary=lambda: product_pricecomponent)

    #: suppliers_info field is added by ProductSupplierInfo class
    #: images field is added by ProductImage class
    #: current_stock field is added by CurrentStockItem class

    def _recalc_price(self, force=False):
        if self.cost and (self.automatic_price or force) and\
                len(self.markup_components):
            self.price = self._calc_price()

    def _calc_price(self):
        price = self.cost
        for comp in self.markup_components:
            price = price * (1 + comp.value/100)
        return price.quantize(dq)

    @hybrid_property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        """Update product price based on new cost value"""
        if self._cost == value:
            return
        self._cost = value
        self._recalc_price()

    @property
    def status_str(self):
        return self._statuses[self.status]

    @property
    def product_type_str(self):
        return self._product_types[self.product_type]

    def __repr__(self):
        return "<Product({0})>".format(self.sku.encode('utf-8'))

    def increase_stock(self, quantity, warehouse, type, unit_cost=None):
        """
        When receiving a product, update the stock reference for this product
        on a specific warehouse.

        :param quantity: amount to increase
        :param warehouse: warehouse that stores this product stock
        :param type: the type of the stock increase. One of
            StockTransaction.types
        :param unit_cost: unit cost of the new stock or `None`
        """
        assert (type in StockTransaction.types)

        if quantity <= 0:
            raise ValueError(u'quantity must be a positive integer')
        if warehouse is None:
            raise ValueError(u'warehouse cannot be None')

        stock = self.stock.filter(ProductStock.warehouse==warehouse).one()
        if stock is None:
            stock = ProductStock(product=self, warehouse=warehouse, quantity=0)
            db.session.add(stock)

        stock.increase_stock(quantity, warehouse, type, unit_cost)

    def decrease_stock(self, quantity, warehouse, type):
        """
        When deliver a product, update the stock reference for the sold item on
        specific warehouse. Returns the stock item that was decreased.

        :params quantity: amount to decrease
        :param warehouse: warehouse that stores this stock
        :param type: the type of the stock decrease. One of
            StockTransaction.types
        """
        assert (type in StockTransaction.types)

        if quantity <= 0:
            raise ValueError(u'quantity must be positive integer')
        if warehouse is None:
            raise ValueError(u'warehouse cannot be None')

        stock = self.stock.filter(ProductStock.warehouse==warehouse).one()

        if stock is None or quantity > stock.quantity:
            raise ValueError(u'quantity to decrease is greater than the '
                             u'available stock.')

        stock.decrease_stock(quantity, warehouse, type)
        return stock

    def register_initial_stock(self, quantity, warehouse, unit_cost):
        """
        Register initial stock, by increasing the amount of this product sotck
        for the given warehouse.

        :param quantity: The initial stock quantity for this product
        :param warehouse: warehouse that stores this stock
        :param unit_cost: The unary cost for the initial stock
        """
        self.increase_stock(quantity, warehouse, StockTransaction.TYPE_INITIAL,
                            unit_cost)

    def get_consolidated_stock(self):
        """
        Returns the stock balance for the product in all warehouses

        :returns: the amount of stock available in al warehouses
        """
        return sum([s.quantity for s in self.stock.all()])

    def get_stock_for_warehouse(self, warehouse):
        """
        Return the stock balance for the product in a certain warehouse

        :params warehouse: warehouse that stores this product
        """
        return self.stock.filter(ProductStock.warehouse==warehouse).one()

    def get_stock_items(self):
        """
        Fetches the product stock items available for all warehouses.
        :returns: a sequence of product stock items
        """
        return self.stock.all()


def product_instances(iter_):
    for obj in iter_:
        if isinstance(obj, Product):
            yield obj


def _try_assert_price(session, flush_context=None, instances=None):
    changed = list(session.new) + list(session.dirty)
    for product in product_instances(changed):
        if product.price is None:
            product._recalc_price()

event.listen(db.session.__class__, 'before_commit', _try_assert_price)


#: listener for Product.automatic_price change
def _product_auto_price_set(target, value, oldvalue, initiator):
    if value and value != oldvalue:
        target._recalc_price(True)

event.listen(Product.automatic_price, 'set', _product_auto_price_set)


class ProductSupplierInfo(db.Model):
    __tablename__ = 'product_supplier_info'

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
                            primary_key=True)
    supplier = db.relationship('Supplier', backref=db.backref('products_info',
                                                        lazy='dynamic'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)
    product = db.relationship('Product', backref=db.backref('suppliers_info',
                                                        lazy='dynamic'))

    #: supplier code for this product
    sku = db.Column(db.Unicode(80))
    #: supplier description for this product
    description = db.Column(db.Unicode, nullable=False)
    #: supplier notes for this product
    notes = db.Column(db.UnicodeText)
    #: supplier base price for this product (list price)
    _base_cost = db.Column('base_cost', db.Numeric(10, 2))
    #: supplier final price for this product (bonus formula applied)
    _cost = db.Column('cost', db.Numeric(10, 2))
    #: use bonus formula to calculate final cost???
    automatic_cost = db.Column(db.Boolean, default=False)

    #: components for automatic final cost calculation
    bonus_components = db.relationship('PriceComponent',
        backref=db.backref("supplier_bonus", lazy='dynamic'),
        secondary=lambda: productsupplierinfo_pricecomponent
    )

    #: the minimum amount that we can buy from this supplier.
    minimum_purchase = db.Column(db.Integer, default=1)
    #: package size to buy this product
    package_size = db.Column(db.Integer, default=1)
    #: number of days needed to deliver the product to purchaser.
    lead_time = db.Column(db.Integer)
    #: When calculate the product cost and we have multiple suppliers for the
    #: same product, this field indicate that we need to use this info for
    #: calculus. A product can have only one main_supplier.
    main_supplier = db.Column(db.Boolean, default=False)

    #: last local update of this information
    last_update = db.Column(db.DateTime, default=datetime.now,
                            onupdate=datetime.now)

    def __repr__(self):
        return "<ProductSupplierInfo({0}, {1})>".format(
                             self.product, self.supplier)

    @hybrid_property
    def base_cost(self):
        return self._base_cost

    @base_cost.setter
    def base_cost(self, value):
        """Update ProductSupplierInfo.cost based on new base_cost"""
        if self._base_cost == value:
            return
        self._recalc_cost()

    @hybrid_property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        """Update product cost"""
        if self._cost == value:
            return
        self._cost = value
        if self.product and self.product.automatic_cost:
            self.product.cost = value

    def _calc_cost(self):
        cost = self.base_cost
        for comp in self.bonus_components:
            cost = cost * (1 - comp.value/100)
        return cost.quantize(dq)

    def _recalc_cost(self, force=False):
        if self.base_cost and (self.automatic_cost or force) and\
                len(self.bonus_components):
            self.cost = self._calc_cost()


#: listener for ProductSupplierInfo.automatic_cost change
def _psi_auto_cost_set(target, value, oldvalue, initiator):
    if value and value != oldvalue:
        target._recalc_cost(True)

event.listen(ProductSupplierInfo.automatic_cost, 'set', _psi_auto_cost_set)


class PriceComponent(db.Model):
    __tablename__ = 'price_component'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    _value = db.Column('value', db.Numeric(10, 2), nullable=False)
    #: supplier_bonus field is added by ProductSupplierInfo.bonus_components
    #: product_markup field is added by Product.markup_components

    @hybrid_property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Update Product/ProductSupplierInfo price/cost on value change"""
        if self._value == value:
            return
        self._value = value
        for product in self.product_markup:
            product._recalc_price()
        for supplier_info in self.supplier_bonus:
            supplier_info._recalc_cost()

    def __repr__(self):
        other = []
        if self.product_markup.count():
            other = self.product_markup.all()
        elif self.supplier_bonus.count():
            other = self.supplier_bonus.all()
        if len(other) > 3:
            other = other[:3] + ['...']
        return "<PriceComponent of {0}, {1}, {2} %>".format(
                repr(other), self.name, self.value)


# Product markup component <--> Price component relation
product_pricecomponent = db.Table('product_pricecomponent', db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'),
              primary_key=True),
    db.Column('price_component_id', db.Integer,
              db.ForeignKey('price_component.id'), primary_key=True)
)

# ProductSupplierInfo bonus component <--> Price component relation
productsupplierinfo_pricecomponent = db.Table(
    'productsupplierinfo_pricecomponent',
    db.Model.metadata,
    db.Column('supplier_id', db.Integer, primary_key=True),
    db.Column('product_id', db.Integer, primary_key=True),
    db.Column('pricecomponent_id', db.Integer,
              db.ForeignKey('price_component.id'), primary_key=True),
    db.ForeignKeyConstraint(
        ['supplier_id',
         'product_id'],
        ['product_supplier_info.supplier_id',
         'product_supplier_info.product_id']),
)


class ProductPriceHistory(db.Model):
    __tablename__ = 'product_price_history'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref='price_history')

    date = db.Column(db.DateTime, default=datetime.now)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return "<ProductPriceHistory({0}, {1}, {2})>".format(
                    self.product,
                    self.date.isoformat() if self.date else "<DATE>",
                    self.price
        )

#: listener for price change
def _product_price_set(target, value, oldvalue, initiator):
    """Creates an entry in product price history table."""
    if oldvalue == value:
        return
    hist = ProductPriceHistory(product=target, price=value)
    db.session.add(hist)

event.listen(Product.price, 'set', _product_price_set)


class ProductUnit(db.Model):
    """Used to represent the |product| unit.
    """
    __tablename__ = 'unit'

    UNIT_TYPE_LENGTH = u'UNIT_TYPE_LENGTH'
    UNIT_TYPE_WEIGHT = u'UNIT_TYPE_WEIGHT'
    UNIT_TYPE_VOLUME = u'UNIT_TYPE_VOLUME'
    UNIT_TYPE_CUSTOM = u'UNIT_TYPE_CUSTOM'

    _unit_types = {
        UNIT_TYPE_LENGTH: u'Longitud',
        UNIT_TYPE_WEIGHT: u'Peso',
        UNIT_TYPE_VOLUME: u'Volumen',
        UNIT_TYPE_CUSTOM: u'Custom',
    }

    id = db.Column(db.Integer, primary_key=True)

    #: The unit description
    description = db.Column(db.Unicode, nullable=False)
    plural = db.Column(db.Unicode)
    abbr = db.Column(db.Unicode, nullable=False)
    allow_fraction = db.Column(db.Boolean, default=False)
    
    unit_type = db.Column(db.Enum(*_unit_types.keys(), name='unit_type_enum'),
                          default=UNIT_TYPE_CUSTOM)

    def __repr__(self):
        return "<ProductUnit({0}, {1})>".format(self.abbr, self.description)


def create_primitive_units():
    units = [
        ProductUnit(description=u'Metro', plural=u'Metros', abbr=u'm',
             allow_fraction=True, unit_type=ProductUnit.UNIT_TYPE_LENGTH),
        ProductUnit(description=u'Kilogramo', plural=u'Kilogramos', abbr=u'kg',
             allow_fraction=True, unit_type=ProductUnit.UNIT_TYPE_WEIGHT),
        ProductUnit(description=u'Litro', plural=u'Litros', abbr=u'l',
             allow_fraction=True, unit_type=ProductUnit.UNIT_TYPE_VOLUME),
        ProductUnit(description=u'Unidad', plural=u'Unidades', abbr=u'u',
             allow_fraction=False, unit_type=ProductUnit.UNIT_TYPE_CUSTOM),
    ]
    db.session.add_all(units)
    db.session.commit()
    print(u'Added basic unit types: Metro, Kilogramo, Litro, Unidad.')


class ProductImage(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Unicode, nullable=False)
    is_main = db.Column(db.Boolean, default=False)

    products = db.relationship(Product, backref='images',
                               secondary=lambda: product_image)


product_image = db.Table('product_image', db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'),
              primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'),
              primary_key=True)
)
