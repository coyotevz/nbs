# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from nbs.models._sqlite_numeric import Numeric

db = SQLAlchemy()
db.Numeric = Numeric

__all__ = ['db', 'User', 'Role', 'Permission', 'ProductCategory', 'Product',
    'ProductSupplierInfo', 'PriceComponent', 'ProductUnit', 'ProductImage',
    'ProductStock', 'Branch', 'Warehouse', 'Office', 'Contact', 'Address',
    'Email', 'Phone', 'ExtraField', 'Supplier', 'SupplierContact',
    'TaxConstant',

    # Documents
    'Document', 'DocumentItem', 'SaleInvoice', 'PurchaseInvoice', 'SaleOrder',
    'PurchaseOrder', 'SaleQuotation', 'PurchaseQuotation', 'SaleRefer',
    'PurchaseRefer', 'SaleCreditNote', 'PurchaseCreditNote', 'SaleDebitNote',
    'PurchaseDebitNote','SaleReceipt', 'PurchaseReceipt', 'SaleReturn',
    'PurchaseReturn', 'PaymentOrder', 'CreditCupon', 'SupplyRequest',
    'StockRequest', 'SupplyTransfer', 'StockTransfer',
]

def configure_db(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    Document, SaleInvoice, PurchaseInvoice, SaleOrder, PurchaseOrder,
    SaleQuotation, PurchaseQuotation, SaleRefer, PurchaseRefer, SaleCreditNote,
    PurchaseCreditNote, SaleDebitNote, PurchaseDebitNote, SaleReceipt,
    PurchaseReceipt, SaleReturn, PurchaseReturn, PaymentOrder, CreditCupon,
    SupplyRequest, StockRequest, SupplyTransfer, StockTransfer
)
