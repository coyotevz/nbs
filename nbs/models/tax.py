# -*- coding: utf-8 -*-

from nbs.models import db

class TaxConstant(db.Model):
    __tablename__ = 'tax_constant'

    #: used for sale operations
    OPERATION_SALE = 'OPERATION_SALE'

    #: used for purchase operation
    OPERATION_PURCHASE = 'OPERATION_PURCHASE'

    #: used for other operations
    OPERATION_OTHER = 'OPERATION_OTHER'

    _operation_types = {
        OPERATION_SALE: 'Venta',
        OPERATION_PURCHASE: 'Compra',
        OPERATION_OTHER: 'Otras operaciones',
    }

    id = db.Column(db.Integer, primary_key=True)

    #: name for this tax
    name = db.Column(db.Unicode, nullable=False)

    #: tax description
    description = db.Column(db.UnicodeText)

    #: applicable tax value
    value = db.Column(db.Numeric(10, 4), nullable=False)

    #: operation type
    operation_type = db.Column(db.Enum(*list(_operation_types.keys()),
                                       name='tax_constant_operation_type'),
                               default=OPERATION_SALE)

    @property
    def operation_type_str(self):
        return self._operation_types[self.operation_type]
