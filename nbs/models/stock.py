# -*- coding: utf-8 -*-

from datetime import datetime

from nbs.models import db
from nbs.models.misc import TimestampMixin
from nbs.utils import dq


class CurrentStock(db.Model, TimestampMixin):
    __tablename__ = 'current_stock'

    #: Product that this stock belong
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)
    product = db.relationship('Product', backref=db.backref('current_stock',
                                                            lazy='dynamic'))

    #: branch which this current stock is stored
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'),
                          primary_key=True)
    branch = db.relationship('Branch', backref='current_stocks')

    #: quatity for this stock item
    quantity = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return "<CurrentStock({0}, {1}, quantity={2})>".format(
                    self.product, self.branch, self.quantity)
