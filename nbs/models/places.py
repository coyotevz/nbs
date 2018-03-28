# -*- coding: utf-8 -*-

from nbs.models import db
from nbs.models.entity import Entity


class Place(Entity):
    __tablename__ = 'place'
    place_id = db.Column(db.Integer, db.ForeignKey('entity.id'),
                         primary_key=True)

    name = Entity._name_1
    responsible_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    responsible = db.relationship('User', lazy='joined',
                            primaryjoin="User.user_id==Place.responsible_id")
    
    __mapper_args__ = {'polymorphic_identity': 'place'}

    def __repr__(self):
        return "<{0}({1})>".format(self.__class__.__name__,
                                   self.name.encode('utf-8'))


class Warehouse(Place):
    __tablename__ = 'warehouse'
    __mapper_args__ = {'polymorphic_identity': 'warehouse'}

    warehouse_id = db.Column(db.Integer, db.ForeignKey('place.place_id'),
                             primary_key=True)


class Branch(Place):
    __tablename__ = 'branch'
    __mapper_args__ = {'polymorphic_identity': 'branch'}

    branch_id = db.Column(db.Integer, db.ForeignKey('place.place_id'),
                          primary_key=True)

    #: Fiscal Point of Sale
    fiscal_pos = db.Column(db.Integer, nullable=False, unique=True)

    warehouse_id = db.Column(db.Integer,
                             db.ForeignKey('warehouse.warehouse_id'))
    warehouse = db.relationship(Warehouse, foreign_keys=warehouse_id)


class Office(Place):
    __tablename__ = 'office'
    __mapper_args__ = {'polymorphic_identity': 'office'}

    office_id = db.Column(db.Integer, db.ForeignKey('place.place_id'),
                          primary_key=True)
