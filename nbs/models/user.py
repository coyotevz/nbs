# -*- coding: utf-8 -*-

from datetime import datetime

from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import BaseQuery

from nbs.models import db
from nbs.models.entity import Entity


class UserQuery(BaseQuery):

    def authenticate(self, login, password):
        if not (password and login):
            return None, False
        user = self.filter(User.username==login).first()
        return user, (user.check_password(password) if user else False)


class User(Entity):
    __tablename__ = 'user'
    __mapper_args__ = {'polymorphic_identity': 'user'}

    query_class = UserQuery

    user_id = db.Column(db.Integer, db.ForeignKey('entity.id'),
                        primary_key=True)

    first_name = Entity._name_1
    last_name = Entity._name_2

    username = db.Column(db.Unicode(60), unique=True, nullable=False)

    # auto role & permissions
    roles = db.relationship('Role', secondary=lambda: userrole_table,
                            lazy='joined', backref='users')
    permissions = db.relationship('Permission',
                                  secondary=lambda: userpermission_table,
                                  lazy='joined', backref='users')

    _pw_hash = db.Column('pw_hash', db.Unicode(80))

    @hybrid_property
    def password(self):
        return self._pw_hash

    @password.setter
    def password(self, password):
        self._pw_hash = str(generate_password_hash(password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def has_role(self, role):
        if isinstance(role, str):
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    def has_permission(self, resource, action):
        """Return if this user has determined permission"""
        for role in self.roles:
            if role.has_permission(resource, action):
                return True
        for perm in self.permissions:
            if perm.resource == resource and perm.action == action:
                return True
        return False

    def __repr__(self):
        return "<User '{0}'>".format(self.username)


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.UnicodeText)

    permissions = db.relationship('Permission',
                                  secondary=lambda: rolepermission_table,
                                  lazy='joined', backref='roles')

    def has_permission(self, resource, action):
        """Return if this role has determined permission"""
        if self.name.lower() == 'superuser':
            return True
        for perm in self.permissions:
            if perm.resource == resource and perm.action == action:
                return True
        return False

    def __repr__(self):
        return "<Role '{0}'>".format(self.name)


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.Unicode(80), nullable=False)
    action = db.Column(db.Unicode(80), nullable=False)

    def __init__(self, resource, action):
        self.resource = resource
        self.action = action

    def __repr__(self):
        return "<Permission({0}, {1})>".format(self.resource, self.action)


userpermission_table = db.Table('user_permission', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'),
              primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'),
              primary_key=True)
)

userrole_table = db.Table('user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'),
              primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'),
              primary_key=True)
)

rolepermission_table = db.Table('role_permission', db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'),
              primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'),
              primary_key=True)
)

def create_admin_user():
    admin = User(username='admin', password='admin', first_name='Admin')
    admin_role = Role(name='superuser', description='Administration Role')
    admin.roles.append(admin_role)
    db.session.add(admin)
    db.session.commit()
    print('Init first session with username: admin, password: admin')
