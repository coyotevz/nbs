# -*- coding: utf-8 -*-

from datetime import datetime
from collections import namedtuple

from nbs.models import db
from nbs.models.misc import TimestampMixin
from nbs.models.places import Place
from nbs.utils import dq


"""
Un documento representa una operación especifica del negocio.
El documento puede contener items que representan los productos que se
involucran en la operación y sus condiciones.
Existen muchos tipos de documentos en función de la operación realizada.
En una operación se pueden utilizar más de un documento.
Ej: Venta pago diferido: Orden de Venta -> Factura -> Remito -> Recibo de pago
Ej: Venta pago contado: Factura

Generalmente los documentos tienen una fecha de emision y lugar de emision,
tambien puden contener una fecha de vencimiento.
"""

SubDoc = namedtuple('SubDoc', 'long short')

SUBTYPE_DOCUMENTS = {
    'NFA': SubDoc(u'Nuestra Factura A', u'Factura A'),
    'NFB': SubDoc(u'Nuestra Factura B', u'Factura B'),
    'VFA': SubDoc(u'Vuestra Factura A', u'Factura A'),
    'VFB': SubDoc(u'Vuestra Factura B', u'Factura B'),
    'VFM': SubDoc(u'Vuestra Factura M', u'Factura M'), # Monotributista
    'NOV': SubDoc(u'Nuestra Orden de Venta', u'Orden de Venta'),
    'NOC': SubDoc(u'Nuestra Orden de Compra', u'Orden de Compra'),
    'PRE': SubDoc(u'Presupuesto de Venta', u'Presupuesto'),
    'PRC': SubDoc(u'Presupuesto de Compra', u'Presupuesto'),
    'REV': SubDoc(u'Remito de Venta', u'Remito'),
    'REC': SubDoc(u'Remito de Compra', u'Remito'),
}


class Document(db.Model, TimestampMixin):
    """Base document"""
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.Unicode)

    subtype_document = db.Column(db.Enum(*SUBTYPE_DOCUMENTS.keys(),
                                         name='subtype_document_enum'),
                                 nullable=False)

    issue_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'),
                               nullable=False)
    issue_place = db.relationship(Place, backref="documents")

    issue_date = db.Column(db.DateTime, default=datetime.now)
    expiration_date = db.Column(db.DateTime, default=datetime.now)
    __mapper_args__ = {'polymorphic_on': document_type}


class DocumentItem(db.Model):
    __tablename__ = 'document_item'
    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    document = db.relationship(Document, backref='items')


# Factura de Venta
class SaleInvoice(Document):
    """A sale invoice is a sale document and contains sale items"""
    __tablename__ = 'sale_invoice'
    __mapper_args__ = {'polymorphic_identity': u'sale_invoice'}
    invoice_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                           primary_key=True)


# Factura de Compra
class PurchaseInvoice(Document):
    __tablename__ = 'purchase_invoice'
    __mapper_args__ = {'polymorphic_identity': u'purchase_invoice'}
    invoice_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                           primary_key=True)


# Orden de Venta
class SaleOrder(Document):
    __tablename__ = 'sale_order'
    __mapper_args__ = {'polymorphic_identity': u'sale_order'}
    order_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                         primary_key=True)


# Orden de Compra
class PurchaseOrder(Document):
    __tablename__ = 'purchase_order'
    __mapper_args__ = {'polymorphic_identity': u'purchase_order'}
    order_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                         primary_key=True)


# Presupuesto de Venta
class SaleQuotation(Document):
    __tablename__ = 'sale_quotation'
    __mapper_args__ = {'polymorphic_identity': u'sale_quotation'}
    quotation_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                             primary_key=True)


# Presupuesto de Compra
class PurchaseQuotation(Document):
    __tablname__ = 'purchase_quotation'
    __mapper_args__ = {'polymorphic_identity': u'purchase_quotation'}
    quotation_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                             primary_key=True)


# Remito de Venta
class SaleRefer(Document):
    __tablename__ = 'sale_refer'
    __mapper_args__ = {'polymorphic_identity': u'sale_refer'}
    refer_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                         primary_key=True)


# Remito de Compra
class PurchaseRefer(Document):
    __tablename__ = 'purchase_refer'
    __mapper_args__ = {'polymorphic_identity': u'purchase_refer'}
    refer_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                         primary_key=True)


# Nota de Crédito de Venta
class SaleCreditNote(Document):
    __tablename__ = 'sale_credit_note'
    __mapper_args__ = {'polymorphic_identity': u'sale_credit_note'}
    note_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                        primary_key=True)


# Nota de Crédito de Compra
class PurchaseCreditNote(Document):
    __tablename__ = 'purchase_credit_note'
    __mapper_args__ = {'polymorphic_identity': u'purchase_credit_note'}
    note_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                        primary_key=True)


# Nota de Débito de Venta
class SaleDebitNote(Document):
    __tablename__ = 'sale_debit_note'
    __mapper_args__ = {'polymorphic_identity': u'sale_debit_note'}
    note_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                        primary_key=True)


# Nota de Débito de Compra
class PurchaseDebitNote(Document):
    __tablename__ = 'purchase_debit_note'
    __mapper_args__ = {'polymorphic_identity': u'purchase_debit_note'}
    note_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                        primary_key=True)


# Recibo de Pago de Venta
class SaleReceipt(Document):
    __tablename__ = 'sale_receipt'
    __mapper_args__ = {'polymorphic_identity': u'sale_receipt'}
    receipt_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                           primary_key=True)


# Recibo de Pago de Compra
class PurchaseReceipt(Document):
    __tablename__ = 'purchase_receipt'
    __mapper_args__ = {'polymorphic_identity': u'purchase_receipt'}
    receipt_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                           primary_key=True)


# Devolución de Venta
class SaleReturn(Document):
    __tablename__ = 'sale_return'
    __mapper_args__ = {'polymorphic_identity': u'sale_return'}
    return_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                          primary_key=True)


# Devolución de Compra
class PurchaseReturn(Document):
    __tablename__ = 'purchase_return'
    __mapper_args__ = {'polymorphic_identity': u'purchase_return'}
    return_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                          primary_key=True)


# Orden de Pago
class PaymentOrder(Document):
    __tablename__ = 'payment_order'
    __mapper_args__ = {'polymorphic_identity': u'payment_order'}
    order_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                         primary_key=True)


# Cupón de Credito (venta)
class CreditCupon(Document):
    __tablename__ = 'credit_cupon'
    __mapper_args__ = {'polymorphic_identity': u'credit_cupon'}
    cupon_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                         primary_key=True)


# Solicitud de Suministro (interno)
class SupplyRequest(Document):
    __tablename__ = 'supply_request'
    __mapper_args__ = {'polymorphic_identity': u'supply_request'}
    request_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                           primary_key=True)


# Solicitud de Mercadería (interno)
class StockRequest(Document):
    __tablename__ = 'stock_request'
    __mapper_args__ = {'polymorphic_identity': u'stock_request'}
    request_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                           primary_key=True)


class SupplyTransfer(Document):
    __tablename__ = 'supply_transfer'
    __mapper_args__ = {'polymorphic_identity': u'supply_transfer'}
    transfer_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                            primary_key=True)


# Transferencia Interna de Mercadería
class StockTransfer(Document):
    __tablename__ = 'stock_transfer'
    __mapper_args__ = {'polymorphic_identity': u'stock_transfer'}
    transfer_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                            primary_key=True)

    source_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'),
                          nullable=False)
    source = db.relationship('Warehouse', backref='transfers_from',
                             foreign_keys=[source_id])

    target_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'),
                          nullable=False)
    target = db.relationship('Warehouse', backref='transfer_to',
                             foreign_keys=[target_id])
