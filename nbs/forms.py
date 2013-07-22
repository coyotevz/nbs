# -*- coding: utf-8 -*-

import decimal

from wtforms.ext.sqlalchemy.orm import model_form
from flask.ext.wtf import (
    Form, HiddenField, BooleanField, TextField, PasswordField, SubmitField,
    DecimalField, Required, NumberRange
)

from .models import db, User, Product


class LoginForm(Form):
    next = HiddenField()

    remember = BooleanField("Remember me")
    username = TextField("Username", validators=[
                    Required(message='You must provide an email or username')
    ])
    password = PasswordField("Password", validators=[
                    Required(message='You must provide a password')
    ])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        rv = super(LoginForm, self).validate()
        if not rv:
            return False

        user, check = User.query.authenticate(self.username.data,
                                              self.password.data)

        if not user or not check:
            self.errors.setdefault('form', []).append("Ivalid data")
            return False

        self.user = user
        return True


ProductForm = model_form(Product, db.session, Form,
    field_args={
        'price': { 'validators': [Required(), NumberRange(min=0)] },
    },
    exclude=[
        'id', '_cost', 'unit', 'category', 'tax_constant', 'suppliers_info',
        'markup_components', 'images'
    ])
