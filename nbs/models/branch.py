# -*- coding: utf-8 -*-

from nbs.models import db


class Branch(db.Model):
    __tablename__ = 'branch'

    branch_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode, nullable=False)

    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manager = db.relationship('User', lazy='dynamic')
