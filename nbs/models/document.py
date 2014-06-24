# -*- coding: utf-8 -*-

from datetime import datetime
from collections import namedtuple

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr

from nbs.models import db
from nbs.models.product import Product
from nbs.models.supplier import Supplier
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


class NumberedDocumentMixin(object):

    number = db.Column(db.Integer)
    issue_place_id = db.Column(db.Integer,
                               db.ForeignKey('document.issue_place_id'))

    __table_args__ = (
        UniqueConstraint('number', 'issue_place_id'),
    )


class FiscalDocumentMixin(object):

    # TODO: fiscal_type_label -> Single letter 'A' or 'B'
    #       fiscal_type_str   -> Complete 'Factura A', 'Nota de Crédito B', etc

    #: Fiscal type 'A' for 'Responsable Inscripto' customer
    FISCAL_TYPE_A = u'FISCAL_A'

    #: Fiscal type 'B' for 'Consumidor Final' customer
    FISCAL_TYPE_B = u'FISCAL_B'

    _fiscal_type = {
        FISCAL_TYPE_A: u'A',
        FISCAL_TYPE_B: u'B',
    }

    fiscal_type = db.Column(db.Enum(*_fiscal_type.keys(),
                                    name='document_fiscal_type'),
                            default=FISCAL_TYPE_B,
                            nullable=False)

    #: Document number, can came from Fiscal Controller, must be unique
    number = db.Column(db.Integer)

    #: copy issue_place_id from parent document for UniqueConstraint
    @declared_attr
    def issue_place_id(cls):
        return db.Column(db.Integer, db.ForeignKey('document.issue_place_id'))

    __table_args__ = (
        UniqueConstraint('fiscal_type', 'number', 'issue_place_id'),
    )

    @property
    def fiscal_type_str(self):
        return self._fiscal_type[self.fiscal_type]


class DocumentItem(db.Model):
    """A line item that can be contained in document model."""
    __tablename__ = 'document_item'
    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Numeric(10, 2))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, backref=db.backref('items',
                                                          lazy='dynamic'))


class SaleDocument(Document):
    """A sale document that is involved in sale operation, contains sale items
    and customer data.
    """
    __tablename__ = 'sale_document'
    __mapped_args__ = {'polymorphic_identity': u'sale_document'}
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                            primary_key=True)

    #customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'),
    #                        nullable=False)
    #customer = db.relationship(Customer, backref="documents")

    #: items collection field added by SaleDocumentItem

    def get_items(self):
        return self.items.all()


class SaleDocumentItem(DocumentItem):
    __tablename__ = 'sale_document_item'
    item_id = db.Column(db.Integer, db.ForeignKey('document_item.id'),
                        primary_key=True)

    document_id = db.Column(db.Integer,
                            db.ForeignKey('sale_document.document_id'),
                            nullable=False)
    document = db.relationship(SaleDocument,
                               backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return "<SaleItem #{} (quantity={}, product={})>".format(self.id,
                self.quantity, self.product_id)


# Factura de Venta
class SaleInvoice(FiscalDocumentMixin, SaleDocument):
    """A sale invoice is a sale document and contains sale items"""
    __tablename__ = 'sale_invoice'
    __mapper_args__ = {'polymorphic_identity': u'sale_invoice'}

    invoice_id = db.Column(db.Integer,
                           db.ForeignKey('sale_document.document_id'),
                           primary_key=True)


    ##: Fiscal type 'A' for 'Responsable Inscripto' customer
    #FISCAL_TYPE_A = u'FISCAL_A'

    ##: Fiscal type 'B' for 'Consumidor Final' customer
    #FISCAL_TYPE_B = u'FISCAL_B'

    #_fiscal_type = {
    #    FISCAL_TYPE_A: u'A',
    #    FISCAL_TYPE_B: u'B',
    #}

    ##: copy issue_place_id from parent document for UniqueConstraint
    #issue_place_id = db.Column(db.Integer,
    #                           db.ForeignKey('document.issue_place_id'))

    ##: invoice type can be 'A' or 'B'
    #fiscal_type = db.Column(db.Enum(*_fiscal_type.keys(),
    #                                name='sale_invoice_fiscal_type'),
    #                        default=FISCAL_TYPE_B,
    #                        nullable=False)

    ##: Invoice number, generally this data came from Fiscal Controller
    #number = db.Column(db.Integer)

    #__table_args__ = (
    #    UniqueConstraint('fiscal_type', 'number', 'issue_place_id'),
    #)

    #@property
    #def fiscal_type_str(self):
    #    return self._fiscal_type[self.fiscal_type]

    def __repr__(self):
        return "<SaleInvoice '{}' {}-{} with {} items>".format(
                self.fiscal_type_str, self.issue_place.fiscal_pos, self.number,
                self.items.count())


# Orden de Venta
class SaleOrder(SaleDocument):
    __tablename__ = 'sale_order'
    __mapper_args__ = {'polymorphic_identity': u'sale_order'}
    order_id = db.Column(db.Integer,
                         db.ForeignKey('sale_document.document_id'),
                         primary_key=True)
    number = db.Column(db.Integer)

    __table_args = (
        UniqueConstraint('number', 'issue_place_id'),
    )


# Presupuesto de Venta
class SaleQuotation(SaleDocument):
    __tablename__ = 'sale_quotation'
    __mapper_args__ = {'polymorphic_identity': u'sale_quotation'}
    quotation_id = db.Column(db.Integer,
                             db.ForeignKey('sale_document.document_id'),
                             primary_key=True)
    number = db.Column(db.Integer)


# Remito de Venta
class SaleRefer(SaleDocument):
    __tablename__ = 'sale_refer'
    __mapper_args__ = {'polymorphic_identity': u'sale_refer'}
    refer_id = db.Column(db.Integer,
                         db.ForeignKey('sale_document.document_id'),
                         primary_key=True)
    number = db.Column(db.Integer)


# Devolución de Venta
class SaleReturn(SaleDocument):
    __tablename__ = 'sale_return'
    __mapper_args__ = {'polymorphic_identity': u'sale_return'}
    return_id = db.Column(db.Integer,
                          db.ForeignKey('sale_document.document_id'),
                          primary_key=True)
    number = db.Column(db.Integer)


# Solicitud de Mercadería (interno)
class StockRequest(SaleDocument):
    __tablename__ = 'stock_request'
    __mapper_args__ = {'polymorphic_identity': u'stock_request'}
    request_id = db.Column(db.Integer,
                           db.ForeignKey('sale_document.document_id'),
                           primary_key=True)


# Transferencia de Mercadería (interno)
class StockTransfer(SaleDocument):
    __tablename__ = 'stock_transfer'
    __mapper_args__ = {'polymorphic_identity': u'stock_transfer'}
    transfer_id = db.Column(db.Integer,
                            db.ForeignKey('sale_document.document_id'),
                            primary_key=True)

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


class PurchaseDocumentItem(DocumentItem):
    __tablename__ = 'purchase_document_item'
    item_id = db.Column(db.Integer, db.ForeignKey('document_item.id'),
                        primary_key=True)
    document_id = db.Column(db.Integer,
                            db.ForeignKey('purchase_document.document_id'),
                            nullable=False)
    document = db.relationship(PurchaseDocument, backref='items')


# Factura de Compra
class PurchaseInvoice(PurchaseDocument):
    __tablename__ = 'purchase_invoice'
    __mapper_args__ = {'polymorphic_identity': u'purchase_invoice'}
    invoice_id = db.Column(db.Integer,
                           db.ForeignKey('purchase_document.document_id'),
                           primary_key=True)


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
    refer_id = db.Column(db.Integer, db.ForeignKey('purchase_document.document_id'),
                         primary_key=True)


# Devolución de Compra
class PurchaseReturn(PurchaseDocument):
    __tablename__ = 'purchase_return'
    __mapper_args__ = {'polymorphic_identity': u'purchase_return'}
    return_id = db.Column(db.Integer, db.ForeignKey('purchase_document.document_id'),
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
