# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

from nbs.models import db


class TimestampMixin(object):

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now,
                         onupdate=datetime.now)


class RefEntityMixin(object):

    @declared_attr
    def entity_id(cls):
        return db.Column('entity_id', db.Integer, db.ForeignKey('entity.id'),
                         nullable=False)

    @declared_attr
    def entity(cls):
        name = cls.__name__.lower()
        return db.relationship('Entity',
                               backref=db.backref(name, lazy='joined'),
                               lazy='joined')


class FiscalDataMixin(object):

    FISCAL_CONSUMIDOR_FINAL = u'FISCAL_CONSUMIDOR_FINAL'
    FISCAL_RESPONSABLE_INSCRIPTO = u'FISCAL_RESPONSABLE_INSCRIPTO'
    FISCAL_EXCENTO = u'FISCAL_EXCENTO'
    FISCAL_MONOTRIBUTO = u'FISCAL_MONOTRIBUTO'

    _fiscal_types = {
        FISCAL_CONSUMIDOR_FINAL: u'Consumidor Final',
        FISCAL_RESPONSABLE_INSCRIPTO: u'Responsable Inscripto',
        FISCAL_EXCENTO: u'Excento',
        FISCAL_MONOTRIBUTO: u'Monotributo',
    }

    cuit = db.Column(db.UnicodeText(13))
    fiscal_type = db.Column(db.Enum(*_fiscal_types.keys(),
                                    name='fiscal_type_enum'),
                            default=FISCAL_CONSUMIDOR_FINAL)

    @property
    def display_fiscal_type(self):
        return self._fiscal_types.get(self.fiscal_type, 'Unknown')
    
    @property
    def needs_cuit(self):
        return self.fiscal_type in (self.FISCAL_EXCENTO,
                                    self.FISCAL_RESPONSABLE_INSCRIPTO)


class Address(RefEntityMixin, db.Model):
    """Stores addresses information"""
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.Unicode)
    street = db.Column(db.Unicode(128), nullable=False)
    city = db.Column(db.Unicode(64))
    province = db.Column(db.Unicode(32), nullable=False)
    postal_code = db.Column(db.Unicode(32))

    def __str__(eslf):
        retval = unicode(self.street)
        if self.city:
            retval += ", {}".format(self.city)
        retval += ", {}".format(self.province)
        if self.postal_code:
            retval += " ({})".format(self.postal_code)
        return retval


class Phone(RefEntityMixin, db.Model):
    """Model to store phone information"""
    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True)
    phone_type = db.Column(db.Unicode)
    prefix = db.Column(db.Unicode(8))
    number = db.Column(db.Unicode, nullable=False)
    extension = db.Column(db.Unicode(5))

    def __str__(self):
        retval = unicode(self.phone_type+': ' if self.phone_type else '')
        if self.prefix:
            retval += "({})".format(self.prefix)
        retval += self.number
        if self.extension:
            retval += " ext: {}".format(self.extension)
        return retval


class Email(RefEntityMixin, db.Model):
    """Model to store email information"""
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    email_type = db.Column(db.Unicode(50))
    email = db.Column(db.Unicode(50), nullable=False)

    def __str__(self):
        retval = self.email_type + ': ' if self.email_type else ''
        retval += self.email
        return retval


class ExtraField(RefEntityMixin, db.Model):
    """Model to store information of additional data"""
    __tablename__ = 'extra_field'
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.Unicode(50), nullable=False)
    field_value = db.Column(db.Unicode(50), nullable=False)

    def __str__(self):
        return self.field_type + ': ' + self.field_value
