# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import event

from nbs.models import db
from nbs.models.misc import TimestampMixin
from nbs.utils import dq


class StockCost(db.Model, TimestampMixin):
    """
    Used to track the cost for stock moviments and valuations. This differs
    from Product.cost that is used to calculate final sale price.
    """
    __tablename__ = 'stock_cost'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)
    product = db.relationship('Product',
                              backref=db.backref('stock_cost', uselist=False))
    cost = db.Column(db.Numeric(10, 2), default=0)

    def get_history(self):
        return db.session.query(StockCostHistory)\
                         .filter(StockCostHistory.stock_cost==self)\
                         .order_by(StockCostHistory.created.desc())\
                         .all()

    def __repr__(self):
        return "<StockCost({0}, {1})>".format(self.product, self.cost)


class StockCostHistory(db.Model):
    """
    Used to track changes on StockCost model.
    """
    __tablename__ = 'stock_cost_history'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    cost = db.Column(db.Numeric(10, 2), nullable=False)

    stock_cost_id = db.Column(db.Integer,
                              db.ForeignKey('stock_cost.product_id'))
    stock_cost = db.relationship(StockCost)

    def __repr__(self):
        return "<StockCostHistory({0}, {1}, {2})>".format(
                    self.stock_cost.product,
                    self.cost,
                    self.created
        )


def _stock_cost_set(target, value, oldvalue, initiator):
    """Creates an entry in stock cost history table."""
    if oldvalue == value:
        return
    hist = StockCostHistory(stock_cost=target, cost=value)
    db.session.add(hist)

event.listen(StockCost.cost, 'set', _stock_cost_set)


class ProductStock(db.Model, TimestampMixin):
    __tablename__ = 'product_stock'

    #: Product that this stock belong
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)
    product = db.relationship('Product', backref='stock')
    product_query = db.relationship('Product',
                                    backref=db.backref('stock_query',
                                                       lazy="dynamic"))

    #: warehouse which the stock is stored
    warehouse_id = db.Column(db.Integer,
                             db.ForeignKey('warehouse.warehouse_id'),
                             primary_key=True)
    warehouse = db.relationship('Warehouse', backref='stocks')

    #: current quantity for this stock item
    quantity = db.Column(db.Numeric(10, 2), nullable=False)

    #: logic quantity for this stock item
    logic_quantity = db.Column(db.Numeric(10, 2))

    #: 'transactions' field added by StockTransaction class

    def __init__(self, *args, **kwargs):
        super(ProductStock, self).__init__(*args, **kwargs)
        if self.product.stock_cost is None:
            StockCost(product=self.product)

    def __repr__(self):
        return "<ProductStock({0}, {1}, quantity={2})>".format(
                    self.product, self.warehouse, self.quantity)


    def increase_stock(self, quantity, warehouse, type, unit_cost=None):
        assert (type in StockTransaction.types)

        if unit_cost is not None:
            self.update_cost(quantity, unit_cost)

        cost = self.product.stock_cost.cost

        old_quantity = self.quantity
        self.quantity += quantity

        st = StockTransaction(product_stock=self, quantity=quantity,
                              type=type, stock_cost=cost)
        db.session.add(st)

    def decrease_stock(self, quantity, warehouse, type):
        assert (type in StockTransaction.types)

        old_quantity = self.quantity
        self.quantity -= quantity

        cost = self.product.stock_cost.cost

        st = StockTransaction(product_stock=self, quantity=quantity,
                              type=type, stock_cost=cost)
        db.session.add(st)

    def update_cost(self, quantity, unit_cost):
        """
        Update the cost for this stock according selected policy.

        Note: By the moment we only implement 'averange cost' valuation policy.
        """
        cost = self.product.stock_cost.cost
        if not self.quantity:
            total_cost = 0
        else:
            total_cost = self.quantity * cost
        total_cost += quantity * unit_cost
        total_items = self.quantity + quantity
        self.product.stock_cost.cost = total_cost / total_items


    def get_transactions(self):
        """
        Shortcut that returns a list of StockTransactions for this product
        stock.
        """
        return self.transactions.all()


class StockTransaction(db.Model):
    """This class stores information about all transactions made in the stock

    Everytime a product has stock increased or decresed, an object of this
    class will be created, registering the quantity, cost, responsible and
    reason for the transaction.
    """
    __tablename__ = 'stock_transaction'

    #: the transaction is an initial stock adjustment. Note that with whis
    #: transaction, there is no related object.
    TYPE_INITIAL = u'TYPE_INITIAL'

    #: the transaction is a sale
    TYPE_SALE = u'TYPE_SALE'

    #: the transaction is a return of a sale
    TYPE_RETURNED_SALE = u'TYPE_RETURNED_SALE'

    #: the transaction is the cancellation of a sale
    TYPE_CANCELED_SALE = u'TYPE_CANCELED_SALE'

    #: the transaction is the receival of a purchase
    TYPE_RECEIVED_PURCHASE = u'TYPE_RECEIVED_PURCHASE'

    #: the transaction is a return of a purchase
    TYPE_RETURNED_PURCHASE = u'TYPE_RETURNED_PURCHASE'

    #: the transaction is the receival of a purchase
    TYPE_RETURNED_LOAN = u'TYPE_RETURNED_LOAN'

    #: the transaction is a loan
    TYPE_LOANED = u'TYPE_LOANED'

    #: the transaction is a stock decrease
    TYPE_STOCK_DECREASE = u'TYPE_STOCK_DECREASE'

    #: the transaction is a transfer from a branch
    TYPE_TRANSFER_FROM = u'TYPE_TRANSFER_FROM'

    #: the transaction is a transfer to a branch
    TYPE_TRANSFER_TO = u'TYPE_TRANSFER_TO'

    #: the transaction is the adjustment of an inventory
    TYPE_INVENTORY_ADJUST = u'TYPE_INVENTORY_ADJUST'

    #: the transaction is a stock decrease by product failure
    TYPE_FAILURE_DECREASE = u'TYPE_FAILURE_DECREASE'

    types = {
        TYPE_INITIAL: u'Stock inicial',
        TYPE_SALE: u'Venta %s',
        TYPE_RETURNED_SALE: u'Devolución de venta %s',
        TYPE_CANCELED_SALE: u'Devolución por cancelación de venta %s',
        TYPE_RECEIVED_PURCHASE: u'Recepción de compra %s',
        TYPE_RETURNED_PURCHASE: u'Devolución de compra %s',
        TYPE_RETURNED_LOAN: u'Devolución de prestamo',
        TYPE_LOANED: u'Prestamo',
        TYPE_STOCK_DECREASE: u'Disminución de stock %s',
        TYPE_TRANSFER_FROM: u'Transferencia desde %s',
        TYPE_TRANSFER_TO: u'Transferencia hacia %s',
        TYPE_INVENTORY_ADJUST: u'Ajuste por inventario %s',
        TYPE_FAILURE_DECREASE: u'Disminución por Producto fallado %s',
    }

    id = db.Column(db.Integer, primary_key=True)

    #: the date and time the transaction was made
    date = db.Column(db.DateTime, default=datetime.now)

    #: the product stock used in this transaction
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product_stock.product_id'))
    warehouse_id = db.Column(db.Integer,
                             db.ForeignKey('product_stock.warehouse_id'))
    product_stock = db.relationship(
            ProductStock, backref=db.backref('transactions', lazy='dynamic'),
            primaryjoin="and_("
                "StockTransaction.product_id==ProductStock.product_id,"
                "StockTransaction.warehouse_id==ProductStock.warehouse_id)"
    )

    #: the stock cost of the transaction on the time it was made
    stock_cost = db.Column(db.Numeric(10, 2), nullable=False)

    #: The quantity that was removed or added to the stock.
    #: Positive value if the stock was increased, negative if decreased.
    quantity = db.Column(db.Numeric(10, 2), nullable=False)

    #: the loged user responsible for the transaction
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User')

    # TODO line item that produced stock change

    #: the type of transaction
    type = db.Column(db.Unicode, nullable=False)


    def get_description(self):
        """Based on the type of the transaction, returns the string
        description.
        """
        return self.types[self.type]

    def __repr__(self):
        return "<StockTransaction({0}, {1})>".format(self.type, self.quantity)
