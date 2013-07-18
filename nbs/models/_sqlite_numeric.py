# -*- coding: utf-8 -*-

"""
    nbs.models._sqlite_numeric
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement some workaround for use Numeric with SQLite.
"""

import decimal
from sqlalchemy import types

# From: http://www.sqlalchemy.org/trac/ticket/1759
class ShiftedDecimal(types.TypeDecorator):
    impl = types.Integer

    def __init__(self, scale):
        types.TypeDecorator.__init__(self)
        self.scale = scale

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = decimal.Decimal(value).scaleb(self.scale)
            value = int(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = decimal.Decimal(str(value))
            value = value * decimal.Decimal("1E-%d" % self.scale)
        return value

    def copy(self):
        return ShiftedDecimal(self.scale)


# Custom type that implement types.Numeric as ShiftedDecimal for sqlite bakcend
class Numeric(types.TypeDecorator):
    impl = types.Numeric

    def __init__(self, precision=None, scale=None, asdecimal=True):
        types.TypeDecorator.__init__(self, precision, scale, asdecimal)
        if scale is None:
            scale = 2
        self.scale = scale

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return ShiftedDecimal(self.scale)
        return super(Numeric, self).load_dialect_impl(dialect)
