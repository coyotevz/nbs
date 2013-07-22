# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.hybrid import hybrid_property
from nbs.models import db

dq = Decimal('0.01')


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
        return "<ProductCategory('{0}')>".format(self.description)


class Product(db.Model):
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

    #: Last update for this product
    last_update = db.Column(db.DateTime, default=datetime.now,
                            onupdate=datetime.now)

    #: PriceComponents for automatic price calculation
    markup_components = db.relationship('PriceComponent',
            backref=db.backref("product_pricecomponent", lazy='dynamic'),
            secondary=lambda: product_pricecomponent)

    #: suppliers_info field is added by ProductSupplierInfo class
    #: images field is added by ProductImage class

    # listener for cost change, for automatic price recalc
    @hybrid_property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value
        self._recalc_price()

    def _recalc_price(self):
        if self.cost and self.automatic_price and len(self.markup_components):
            self.price = self._calc_price()

    def _calc_price(self):
        price = self.cost
        for comp in self.markup_components:
            price = price * (1 + comp.value/100)
        return price.quantize(dq)

    def increase_stock(self, branch, qty, cost):
        pass

    def decrease_stock(self, branch, qty):
        pass

    @property
    def status_str(self):
        return self._statuses[self.status]

    @property
    def type_str(self):
        return self._product_types[self.product_type]

    def __repr__(self):
        return "<Product({0})>".format(self.sku)


class ProductSupplierInfo(db.Model):
    __tablename__ = 'product_supplier_info'

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),
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
    #: the cost which helps the purchaser to define the main cost of a certain
    #: product. Each product have multiple |suppliers| and for each |supplier|
    #: a base_cost is available. The purchaser in this case must decide how
    #: to define the main cost in the base cost averange of all suppliers.
    base_cost = db.Column(db.Numeric(10, 2))
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
        return '<ProductSupplierInfo(product_id=%s, supplier_id=%s)>' %\
                (self.product_id, self.supplier_id)


class PriceComponent(db.Model):
    __tablename__ = 'price_component'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    _value = db.Column('value', db.Numeric(10, 2), nullable=False)

    @hybrid_property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for product in self.products_markups:
            product._recalc_price()
        for supplier_info in self.supplier_bonifications:
            supplier_info._recalc_cost()


# Product markup component <--> Price component relation
product_pricecomponent = db.Table('product_pricecomponent', db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'),
              primary_key=True),
    db.Column('price_component_id', db.Integer,
              db.ForeignKey('price_component.id'), primary_key=True)
)

# ProductSupplierInfo bonification component <--> Price component relation
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
    description = db.Column(db.Unicode)
    plural = db.Column(db.Unicode)
    abbr = db.Column(db.Unicode)
    allow_fraction = db.Column(db.Boolean, default=False)
    
    unit_type = db.Column(db.Enum(*_unit_types.keys(), name='unit_type_enum'),
                          default=UNIT_TYPE_CUSTOM)


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
