# -*- coding: utf-8 -*-

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr

from nbs.models import db
from nbs.models.places import Warehouse

class NumberedMixin(object):

    number = db.Column(db.Integer)

    @declared_attr
    def issue_place_id(cls):
        return db.Column(db.Integer, db.ForeignKey('document.issue_place_id'))

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint('number', 'issue_place_id'),)

    def __repr__(self):
        return "<{} {}-{}>".format(obj.full_doc_name,
                obj.issue_place.fiscal_pos, obj.number)


class FiscalMixin(object):

    # TODO: fiscal_type_label -> Single letter 'A' or 'B'
    #       fiscal_type_str   -> Complete 'Factura A', 'Nota de Crédito B', etc

    #: Fiscal type 'A' for 'Responsable Inscripto' customer
    FISCAL_TYPE_A = u'FISCAL_A'

    #: Fiscal type 'B' for 'Consumidor Final' customer
    FISCAL_TYPE_B = u'FISCAL_B'

    _fiscal_type = {
        FISCAL_TYPE_A: u'A',
        FISCAL_TYPE_B: u'B',
    }

    fiscal_type = db.Column(db.Enum(*_fiscal_type.keys(),
                                    name='document_fiscal_type'),
                            default=FISCAL_TYPE_B,
                            nullable=False)

    #: Document number, can came from Fiscal Controller, must be unique
    number = db.Column(db.Integer)

    #: copy issue_place_id from parent document for UniqueConstraint
    @declared_attr
    def issue_place_id(cls):
        return db.Column(db.Integer, db.ForeignKey('document.issue_place_id'))

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint('fiscal_type', 'number', 'issue_place_id'),)

    @property
    def fiscal_type_str(self):
        return self._fiscal_type[self.fiscal_type]

    @property
    def doc_name(self):
        return self._name + ' %s' % self.fiscal_type_str

    @property
    def full_doc_name(self):
        return self._full_name + ' %s' % self.fiscal_type_str

    def __repr__(self):
        return "<{} {}-{}>".format(obj.full_doc_name,
                obj.issue_place.fiscal_pos, obj.number)


class ItemizedMixin(object):

    @declared_attr
    def items(cls):
        return db.relationship('DocumentItem', lazy='dynamic')

    def get_items(self):
        return self.items.all()

    def __repr__(self):
        return "<{} width {} items>".format(obj.full_doc_name,
                obj.items.count())


class FiscalItemizedMixin(FiscalMixin, ItemizedMixin):

    def __repr__(self):
        return "<{} {}-{} width {} items>".format(self.full_doc_name,
                self.issue_place.fiscal_pos, self.number, self.items.count())


class NumberedItemizedMixin(NumberedMixin, ItemizedMixin):

    def __repr__(self):
        return "<{} {}-{} width {} items>".format(self.full_doc_name,
                self.issue_place.fiscal_pos, self.number, self.items.count())


class RefCustomerMixin(object):
    "Mixin to use in documents against customers"

    @declared_attr
    def customer_id(cls):
        return db.Column(db.Integer, db.ForeignKey('customer.id'),
                         nullable=False)

    @declared_attr
    def customer(cls):
        return db.relationship('Customer')


class RefSupplierMixin(object):
    "Mixin to use in documents against suppliers"

    @declared_attr
    def supplier_id(cls):
        return db.Column(db.Integer, db.ForeignKey('supplier.id'),
                         nullable=False)

    @declared_attr
    def supplier(cls):
        return db.relationship('Supplier')


class RefBranchesMixin(object):
    "Mixin to use in documents between branches"

    @declared_attr
    def source_id(cls):
        return db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'),
                         nullable=False)

    @declared_attr
    def source(cls):
        return db.relationship(Warehouse,
                primaryjoin=lambda: Warehouse.warehouse_id==cls.source_id)

    @declared_attr
    def target_id(cls):
        return db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'),
                         nullable=False)

    @declared_attr
    def target(cls):
        return db.relationship(Warehouse,
                primaryjoin=lambda: Warehouse.warehouse_id==cls.target_id)
