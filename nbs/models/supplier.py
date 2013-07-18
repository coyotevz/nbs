# -*- coding: utf-8 -*-

from sqlalchemy.ext.associationproxy import association_proxy

from nbs.models import db
from nbs.models.misc import FiscalDataMixin
from nbs.models.product import (
    productsupplierinfo_pricecomponent, PriceComponent, ProductSupplierInfo
)


class Supplier(db.Model, FiscalDataMixin):
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    fancy_name = db.Column(db.Unicode)
    notes = db.Column(db.UnicodeText)
    payment_term = db.Column(db.Integer)
    supplier_contacts = db.relationship('SupplierContact',
                                        cascade='all,delete-orphan',
                                        backref="supplier")
    contacts = association_proxy('supplier_contacts', 'contact')

    #: products_info field added by products.ProductSupplierInfo relationship

    @property
    def display_name(self):
        retval = self.name
        if self.fancy_name:
            retval += u" ({})".format(self.fancy_name)
        return retval

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
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),
                            primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                           primary_key=True)
    role = db.Column(db.Unicode)

    #: 'supplier' attribute is supplied by Supplier.supplier_contacts relation
    contact = db.relationship('Contact', lazy='joined',
                              backref='supplier_contacts')

    def __init__(self, contact, role):
        self.contact = contact
        self.role = role
