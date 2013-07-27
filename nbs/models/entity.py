# -*- coding: utf-8 -*-

from datetime import datetime
from nbs.models import db


class Entity(db.Model):
    """
    Base class for entity submodels.

    An entity is a model that has two names, one required and one optional, and
    a series of addresses, phones, emails and extrafields.
    Model to be suitable to this description are for example User, Employee,
    Supplier, Customer, Contact, Branch, etc.
    """
    __tablename__ = 'entity'

    id = db.Column(db.Integer, primary_key=True)
    _name_1 = db.Column('name_1', db.Unicode, nullable=False)
    _name_2 = db.Column('name_2', db.Unicode)
    entity_type = db.Column(db.Unicode(50))
    notes = db.Column(db.UnicodeText)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    __mapper_args__ = {'polymorphic_on', entity_type}
