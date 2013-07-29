# -*- coding: utf-8 -*-

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from nbs.models import db
from nbs.models.entity import Entity
from nbs.models.misc import FiscalDataMixin
from nbs.models.product import (
    productsupplierinfo_pricecomponent, PriceComponent, ProductSupplierInfo
)


class Supplier(Entity, FiscalDataMixin):
    __tablename__ = 'supplier'
    __mapper_args__ = {'polymorphic_identity': u'supplier'}

    supplier_id = db.Column(db.Integer, db.ForeignKey('entity.id'),
                            primary_key=True)
    name = Entity._name_1
    fancy_name = Entity._name_2

    payment_term = db.Column(db.Integer)
    supplier_contacts = db.relationship('SupplierContact',
                                        cascade='all,delete-orphan',
                                        backref="supplier")
    contacts = association_proxy('supplier_contacts', 'contact')

    #: products_info field added by products.ProductSupplierInfo relationship

    @hybrid_property
    def full_name(self):
        fn = u" ({0})".format(self.fancy_name) if self.fancy_name else u""
        return u"{0}{1}".format(self.name, fn)

    def add_contact(self, contact, role):
        self.supplier_contacts.append(SupplierContact(contact, role))

    def get_related_bonifications(self):
        q = PriceComponent.query.join(productsupplierinfo_pricecomponent)\
                                .join(ProductSupplierInfo)\
                                .join(Supplier)\
                                .filter(Supplier.id==self.id).distinct()
        return q


class SupplierContact(db.Model):
    __tablename__ = 'supplier_contact'
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
                            primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.contact_id'),
                           primary_key=True)
    role = db.Column(db.Unicode)

    #: 'supplier' attribute is supplied by Supplier.supplier_contacts relation
    contact = db.relationship('Contact', lazy='joined',
                              backref='supplier_contacts')

    def __init__(self, contact, role):
        self.contact = contact
        self.role = role
