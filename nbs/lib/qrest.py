# -*- coding: utf-8 -*-

"""
    nbs.lib.rest
    ~~~~~~~~~~~~

    Provides tools for building REST interfaces.
"""

from collections import namedtuple
from sqlalchemy import and_
from flask import request

_keywords = [
    'page', 'per_page', 'single', 'sort', 'fields', 'include'
]

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

#: Represents and "order by" in SQL query expression
OrderBy = namedtuple('OrderBy', 'field direction')

#: Represents a filter to apply to a SQL query
Filter = namedtuple('Filter', 'field operator argument')


class QueryParameters(object):
    """
    Aggregates the parameter for a search, including filters, search type,
    page, per_page and sort directive and fields to retrieve from.
    """

    def __init__(self, fields=None, filters=None, page=None, per_page=None,
                 sort=None, single=False):
        self.fields = fields or []
        self.filters = filters or []
        self.page = page or 1
        self.per_page = per_page or 25
        self.sort = sort or []
        self.single = bool(single)

    def __repr__(self):
        template = ('<QueryParameters fields={}, filters={}, sort={}, '
                    'page={}, per_page={}, single={}>')
        return template.format(self.fields, self.filters, self.sort,
                               self.page, self.per_page, self.single)

    @staticmethod
    def from_dict(data):
        """
        Returns a new :class:`QueryParameters` object with arguments parsed
        from `data`.
        """
        fields = data.pop('fields', [])
        sort = [OrderBy(o[1], o[0]) for o in data.pop('sort', [])]
        page = data.pop('page', None)
        per_page = data.pop('per_page', None)
        single = data.pop('single', False)
        filters = []
        for key, value in data.iteritems():
            filters.extend([Filter(key, f[0], f[1]) for f in value])
        return QueryParameters(fields=fields, filters=filters, page=page,
                               per_page=per_page, sort=sort, single=single)


class SQLQueryBuilder(object):
    """
    Provides static functions for building SQLAlchemy query object based on a
    :class:`QueryParameters` instance.
    """

    @staticmethod
    def create_operation(model, fieldname, operator, argument, relation=None):
        """
        Translates an operation described as string to a valid SQLAlchemy query
        parameter using a field or relation of the model.
        """
        opfunc = OPERATORS[operator]
        field = getattr(model, relation or fieldname)
        return opfunc(field, argument)

    @staticmethod
    def create_filters(model, filters):
        """
        Returns a list of operations on `model` specified in the
        `filters` list.
        """
        nfilters = []
        for f in filters:
            fname = f.fieldname
            relation = None
            if '.' in fname:
                relation, fname = fname.split('.')
            param = SQLQueryBuilder.create_operation(model, fname, f.operator,
                                                     f.argument, relation)
            nfilters.append(param)
        return nfilters

    @staticmethod
    def create_query(model, query_params):

        if not isinstance(query_params, QueryParameters):
            raise ValueError("query_params must be an instance of "
                             "QueryParameters")

        # TODO: Optimize query base on relations required
        query = model.query

        # Adding field filters
        filters = SQLQueryBuilder.create_filters(model, query_params.filters)
        query = query.filter(and_(*filters))

        # Sort query
        for s in query_params.sort:
            field = getattr(model, s.field)
            direction = SORT_ORDER[s.direction](field)
            query = query.order_by(direction())

        return query


def parse_param(key, value):
    key, op = (key.rsplit(':', 1) + ['eq'])[:2]
    if key not in _keywords:
        value = [(op, v) for v in value]
    elif key == 'sort':
        if op not in SORT_ORDER.keys():
            op = 'asc'
        value = [(op, v) for v in value]
    elif key == 'single':
        value = [bool(int(v)) for v in value]
    elif key in ('page', 'per_page'):
        value = [int(v) for v in value]
    return key, value


def unroll_params(params):
    for k in ('page', 'per_page', 'single'):
        if params.has_key(k):
            params[k] = params[k][0]


def get_params():
    params = {}
    for key, value in request.args.iterlists():
        k, v = parse_param(key, value)
        params.setdefault(k, []).extend(v)
    unroll_params(params)
    return QueryParameters.from_dict(params)
