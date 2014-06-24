# -*- coding: utf-8 -*-
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


from datetime import datetime

from nbs.models import db
from nbs.models.product import Product
from nbs.models.supplier import Supplier
from nbs.models.misc import TimestampMixin
from nbs.models.places import Place

from nbs.models.docmixin import (
    NumberedDocumentMixin, FiscalDocumentMixin, ItemizedDocumentMixin,
    RefCustomerMixin, RefSupplierMixin, RefBranchesMixin
)


# Document statuses

class Document(db.Model, TimestampMixin):
    """Base document"""
    __tablename__ = 'document'

    # TODO: Redesign statuses

    #: the document is in draft status
    STATUS_DRAFT = u'STATUS_DRAFT'

    STATUS_PENDING = u'STATUS_PENDING'
    STATUS_CONFIRMED = u'STATUS_CONFIRMED'

    #: this document has been issued and can't be modified
    STATUS_ISSUED = u'STATUS_ISSUED'
    STATUS_CLOSED = u'SATUS_CLOSED'

    _statuses = {
        STATUS_DRAFT: u'Borrador',
        STATUS_PENDING: u'Pendiente',
        STATUS_CONFIRMED: u'Confirmada',
        STATUS_ISSUED: u'Emitido',
        STATUS_CLOSED: u'Cerrado',
    }

    doc_name = u'Unknown'
    full_doc_name = u'Unknown'

    id = db.Column(db.Integer, primary_key=True)

    #: holder for subclass type
    _type = db.Column(db.Unicode)

    issue_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'),
                               nullable=False)
    issue_place = db.relationship(Place, backref="documents")

    issue_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)

    status = db.Column(db.Enum(*_statuses.keys(), name='document_status_enum'),
                       default=STATUS_DRAFT,
                       nullable=False)

    __mapper_args__ = {'polymorphic_on': _type}

    @property
    def status_str(self):
        return self._statuses[self.status]

    # TODO: Verify that issue_date <= expiration_date

    def issue(self):
        self.status = self.STATUS_ISSUED
        self.issue_date = datetime.now()

    def can_modify(self):
        return self.status in (self.STATUS_DRAFT, self.STATUS_PENDING)


class DocumentItem(db.Model):
    """A line item that can be contained in document model."""
    __tablename__ = 'document_item'
    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    document = db.relationship(Document)
    quantity = db.Column(db.Numeric(10, 2))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, backref=db.backref('items',
                                                          lazy='dynamic'))


# Factura de Venta
class SaleInvoice(FiscalDocumentMixin, ItemizedDocumentMixin, Document):
    """A sale invoice is a sale document and contains sale items"""
    __tablename__ = 'sale_invoice'
    _full_name = u'Factura de Venta'
    _name = u'Factura'

    invoice_id = db.Column(db.Integer,
                           db.ForeignKey('document.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': u'sale_invoice',
        'inherit_condition': invoice_id == Document.id
    }

    def __repr__(self):
        return "<SaleInvoice '{}' {}-{} with {} items>".format(
            self.fiscal_type_str, self.issue_place.fiscal_pos, self.number,
            self.items.count()
        )


# Orden de Venta
class SaleOrder(NumberedDocumentMixin, ItemizedDocumentMixin, Document):
    __tablename__ = 'sale_order'
    full_doc_name = u'Orden de Venta'
    doc_name = u'Ordern de Venta'

    order_id = db.Column(db.Integer,
                         db.ForeignKey('document.id'),
                         primary_key=True)
    number = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': u'sale_order',
        'inherit_condition': order_id == Document.id
    }


# Presupuesto de Venta
class SaleQuotation(Document):
    __tablename__ = 'sale_quotation'
    full_doc_name = u'Presupuesto de Venta'
    doc_name = u'Presupuesto'

    quotation_id = db.Column(db.Integer,
                             db.ForeignKey('document.id'),
                             primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': u'sale_quotation',
        'inherit_condition': quotation_id == Document.id
    }


# Remito de Venta
class SaleRefer(Document):
    __tablename__ = 'sale_refer'
    full_doc_name = u'Remito de Venta'
    doc_name = u'Remito'

    refer_id = db.Column(db.Integer,
                         db.ForeignKey('document.id'),
                         primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': u'sale_refer',
        'inherit_condition': refer_id == Document.id
    }


# Devolución de Venta
class SaleReturn(Document):
    __tablename__ = 'sale_return'
    full_doc_name = u'Devolución de Venta'
    doc_name = u'Devolución'

    return_id = db.Column(db.Integer,
                          db.ForeignKey('document.id'),
                          primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': u'sale_return',
        'inherit_condition': return_id == Document.id
    }


# Solicitud de Mercadería (interno)
class StockRequest(Document):
    __tablename__ = 'stock_request'
    full_doc_name = u'Solicitud de Mercadería'
    doc_name = u'Solicitud de Mercadería'

    request_id = db.Column(db.Integer,
                           db.ForeignKey('document.id'),
                           primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': u'stock_request',
        'inherit_condition': request_id == Document.id
    }


# Transferencia de Mercadería (interno)
class StockTransfer(Document):
    __tablename__ = 'stock_transfer'

    transfer_id = db.Column(db.Integer,
                            db.ForeignKey('document.id'),
                            primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': u'stock_transfer',
        'inherit_condition': transfer_id == Document.id
    }

    source_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'),
                          nullable=False)
    source = db.relationship('Warehouse', backref='transfers_from',
                             foreign_keys=[source_id])

    target_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'),
                          nullable=False)
    target = db.relationship('Warehouse', backref='transfer_to',
                             foreign_keys=[target_id])


# Purchase documents
# ~~~~~~~~~~~~~~~~~~
# TODO: clean purchase documents structure

class PurchaseDocument(Document):
    """A purchase document that is involved on purchase process, contains
    purchase items."""
    __tablename__ = 'purchase_document'
    __mapper_args__ = {'polymorphic_identity': u'purchase_document'}
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                            primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
                            nullable=False)
    supplier = db.relationship(Supplier, backref='documents')

    #: items collection added by PurchaseDocumentItem


# Factura de Compra
class PurchaseInvoice(FiscalDocumentMixin, ItemizedDocumentMixin,
                      Document):
    __tablename__ = 'purchase_invoice'
    invoice_id = db.Column(db.Integer,
                           db.ForeignKey('document.id'),
                           primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': u'purchase_invoice',
        'inherit_condition': invoice_id == Document.id,
    }


# Orden de Compra
class PurchaseOrder(PurchaseDocument):
    __tablename__ = 'purchase_order'
    __mapper_args__ = {'polymorphic_identity': u'purchase_order'}
    order_id = db.Column(db.Integer,
                         db.ForeignKey('purchase_document.document_id'),
                         primary_key=True)


# Presupuesto de Compra
class PurchaseQuotation(PurchaseDocument):
    __tablname__ = 'purchase_quotation'
    __mapper_args__ = {'polymorphic_identity': u'purchase_quotation'}
    quotation_id = db.Column(db.Integer,
                             db.ForeignKey('purchase_document.document_id'),
                             primary_key=True)


# Remito de Compra
class PurchaseRefer(PurchaseDocument):
    __tablename__ = 'purchase_refer'
    __mapper_args__ = {'polymorphic_identity': u'purchase_refer'}
    refer_id = db.Column(db.Integer,
                         db.ForeignKey('purchase_document.document_id'),
                         primary_key=True)


# Devolución de Compra
class PurchaseReturn(PurchaseDocument):
    __tablename__ = 'purchase_return'
    __mapper_args__ = {'polymorphic_identity': u'purchase_return'}
    return_id = db.Column(db.Integer,
                          db.ForeignKey('purchase_document.document_id'),
                          primary_key=True)


# Other documents
# ~~~~~~~~~~~~~~~


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


# Transferencia de insumos (interno)
class SupplyTransfer(Document):
    __tablename__ = 'supply_transfer'
    __mapper_args__ = {'polymorphic_identity': u'supply_transfer'}
    transfer_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                            primary_key=True)
