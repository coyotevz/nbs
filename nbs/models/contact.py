# -*- coding: utf-8 -*-

from sqlalchemy.ext.associationproxy import association_proxy

from nbs.models import db
from nbs.models.entity import Entity


class Contact(Entity):
    __tablename__ = 'contact'
    __mapper_args__ = {'polymorphic_identity': 'contact'}

    contact_id = db.Column(db.Integer, db.ForeignKey('entity.id'),
                           primary_key=True)

    first_name = Entity._name_1
    last_name = Entity._name_2

    #: 'suppliers_contacts' attribute is supplied by SupplierContact.contact
    #: relationship, this attributes refers to SupplierContact instance
    suppliers = association_proxy('supplier_contacts', 'supplier')

#    address = db.relationship('Address',
#            backref=db.backref('contact', lazy='dynamic'),
#            secondary=lambda: contact_address)
#
#    phone = db.relationship('Phone',
#            backref=db.backref('contact', lazy='dynamic'),
#            secondary=lambda: contact_phone)
#
#    email = db.relationship('Email',
#            backref=db.backref('contact', lazy='dynamic'),
#            secondary=lambda: contact_email)
#
#    extra_field = db.relationship('ExtraField',
#            backref=db.backref('contact', lazy='dynamic'),
#            secondary=lambda: contact_extrafield)

    # Contactable fields
#    @hybrid_property
#    def has_address(self):
#        return len(self.address) > 0
#
#    @hybrid_property
#    def has_phone(self):
#        return len(self.phone) > 0
#
#    @hybrid_property
#    def has_email(self):
#        return len(self.email) > 0
#
#    @hybrid_property
#    def has_extra_fields(self):
#        return len(self.extra_field) > 0

#contact_address = db.Table('contact_address', db.Model.metadata,
#    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'),
#              primary_key=True),
#    db.Column('address_id', db.Integer, db.ForeignKey('address.id'),
#              primary_key=True)
#)
#
#contact_phone = db.Table('contact_phone', db.Model.metadata,
#    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'),
#              primary_key=True),
#    db.Column('phone_id', db.Integer, db.ForeignKey('phone.id'),
#              primary_key=True)
#)
#
#contact_email = db.Table('contact_email', db.Model.metadata,
#    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'),
#              primary_key=True),
#    db.Column('email_id', db.Integer, db.ForeignKey('email.id'),
#              primary_key=True)
#)
#
#contact_extrafield = db.Table('contact_extrafield', db.Model.metadata,
#    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'),
#              primary_key=True),
#    db.Column('extrafield_id', db.Integer, db.ForeignKey('extra_field.id'),
#              primary_key=True)
#)
