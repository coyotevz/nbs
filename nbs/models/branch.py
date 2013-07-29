# -*- coding: utf-8 -*-

from nbs.models import db
from nbs.models.entity import Entity


class Branch(Entity):
    __tablename__ = 'branch'
    __mapper_args__ = {'polymorphic_identity': u'branch'}

    branch_id = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)

    name = Entity._name_1

    manager_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    manager = db.relationship('User', lazy='joined',
                              primaryjoin="User.user_id==Branch.manager_id")
