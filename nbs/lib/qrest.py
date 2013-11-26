# -*- coding: utf-8 -*-

"""
    nbs.lib.rest
    ~~~~~~~~~~~~

    Provides tools for building REST interfaces.
"""

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


class OrderBy(object):
    """Represents an "order by" in SQL query expression."""

    def __init__(self, field, direction='asc'):
        assert direction in SORT_ORDER.keys()
        self.field = field
        self.direction = direction

    def __repr__(self):
        return '<OrderBy {}, {}>'.format(self.field, self.direction)


class QueryParameters(object):

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
        print 'remain data:', data
        return QueryParameters(fields=fields, filters=filters, page=page,
                               per_page=per_page, sort=sort, single=single)

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
