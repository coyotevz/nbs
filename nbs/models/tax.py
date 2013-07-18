# -*- coding: utf-8 -*-

from nbs.models import db

class TaxConstant(db.Model):
    __tablename__ = 'tax_constant'

    id = db.Column(db.Integer, primary_key=True)

    #: name for this tax
    name = db.Column(db.Unicode, nullable=False)

    #: tax description
    description = db.Column(db.UnicodeText)

    #: applicable tax value
    value = db.Column(db.Numeric(10, 4), nullable=False)
