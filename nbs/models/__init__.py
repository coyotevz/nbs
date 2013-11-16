# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from nbs.models._sqlite_numeric import Numeric

db = SQLAlchemy()
db.Numeric = Numeric

__all__ = ['db', 'User', 'Role', 'Permission', 'ProductCategory', 'Product',
    'ProductSupplierInfo', 'PriceComponent', 'ProductUnit', 'ProductImage',
    'ProductStock', 'Branch', 'Warehouse', 'Office', 'Contact', 'Address',
    'Email', 'Phone', 'ExtraField', 'Supplier', 'SupplierContact',
    'TaxConstant',

    # Documents
    'SaleInvoice', 'PurchaseInvoice', 'SaleOrder', 'PurchaseOrder',
    'SaleQuotation', 'PurchaseQuotation', 'SaleRefer', 'PurchaseRefer',
    'SaleCreditNote', 'PurchaseCreditNote', 'SaleDebitNote',
    'PurchaseDebitNote','SaleReceipt', 'PurchaseReceipt', 'SaleReturn',
    'PurchaseReturn', 'PaymentOrder', 'CreditCupon', 'StockTransfer',
]

def configure_db(app):
    db.init_app(app)

from nbs.models.user import User, Role, Permission
from nbs.models.product import (
    ProductCategory, Product, ProductSupplierInfo, PriceComponent,
    ProductUnit, ProductImage
)
from nbs.models.stock import ProductStock, StockTransaction
from nbs.models.places import Branch, Warehouse, Office
from nbs.models.contact import Contact
from nbs.models.misc import Address, Email, Phone, ExtraField
from nbs.models.supplier import Supplier, SupplierContact
from nbs.models.tax import TaxConstant

from nbs.models.document import (
        SaleInvoice, PurchaseInvoice, SaleOrder, PurchaseOrder, SaleQuotation,
        PurchaseQuotation, SaleRefer, PurchaseRefer, SaleCreditNote,
        PurchaseCreditNote, SaleDebitNote, PurchaseDebitNote, SaleReceipt,
        PurchaseReceipt, SaleReturn, PurchaseReturn, PaymentOrder, CreditCupon,
        StockTransfer
)
