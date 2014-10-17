# -*- coding: utf-8 -*-

from collections import namedtuple
from sqlalchemy.orm.base import _entity_descriptor
from sqlalchemy.exc import InvalidRequestError
from webargs import Arg

OPERATORS = {

    # General comparators
    'eq': lambda f, a: f == a,
    'neq': lambda f, a: f != a,
    'gt': lambda f, a: f > a,
    'gte': lambda f, a: f >= a,
    'lt': lambda f, a: f < a,
    'lte': lambda f, a: f <= a,

    # String operators
    'contains': lambda f, a: f.contains(a),
    'endswith': lambda f, a: f.endswith(a),
    'startswith': lambda f, a: f.startswith(a),
    'like': lambda f, a: f.like(a),
    'ilike': lambda f, a: f.ilike(a),

    # List operators
    'in': lambda f, a: f.in_(a),
    'nin': lambda f, a: ~f.in_(a),

}

SORT_ORDER = {
    # Sort order
    'asc': lambda f: f.asc,
    'desc': lambda f: f.desc,
}

def get_entity(query, key):
    return _entity_descriptor(query._joinpoint_zero(), key)

class Filter(namedtuple('Filter', 'field, operator, argument')):
    __slots__ = ()

    def apply_query(self, query):
        opfunc = OPERATORS[self.operator]
        try:
            entity = get_entity(query, self.field)
        except InvalidRequestError:
            return query
        return query.filter(opfunc(entity, self.argument))

class Fields(object):
    
    def __init__(self, fields):
        if not isinstance(fields, (list, tuple)):
            fields = [fields]
        self._fields = fields

    def apply_query(self, query):
        entities = []
        for f in self._fields:
            try:
                entities.append(get_entity(query, f))
            except InvalidRequestError:
                pass
        if len(entities):
            return query.with_entities(*entities)
        return query

    def __repr__(self):
        return "<Fields (%s)>" % ", ".join(self._fields)


def FieldsArg(default=None):
    fields = []
    if isinstance(default, (list, tuple)):
        fields = default
    return Arg(default=Fields(fields), use=convert_fields)

def QueryArg():
    return Arg(use=convert_query)


# some conversion functions
def convert_list(l):
    return filter(None, l.split(";"))

def convert_query(l):
    filters = convert_list(l)
    return [Filter(*f.split(":")) for f in filters]

def convert_fields(l):
    fields = convert_list(l)
    return Fields(fields)
