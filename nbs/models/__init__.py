# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from nbs.models._sqlite_numeric import Numeric

db = SQLAlchemy()
db.Numeric = Numeric

__all__ = ['db', 'User', 'Role', 'Permission', 'ProductCategory', 'Product',
    'ProductSupplierInfo', 'PriceComponent', 'ProductUnit', 'ProductImage',
    'CurrentStock', 'Branch', 'Contact', 'Address', 'Email', 'Phone',
    'ExtraField', 'Supplier', 'SupplierContact', 'TaxConstant']

def configure_db(app):
    db.init_app(app)

from nbs.models.user import User, Role, Permission
from nbs.models.product import (
    ProductCategory, Product, ProductSupplierInfo, PriceComponent,
    ProductUnit, ProductImage
)
from nbs.models.stock import CurrentStock
from nbs.models.branch import Branch
from nbs.models.contact import Contact
from nbs.models.misc import Address, Email, Phone, ExtraField
from nbs.models.supplier import Supplier, SupplierContact
from nbs.models.tax import TaxConstant
