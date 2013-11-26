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
    'asc': lambda f: f.asc,
    'desc': lambda f: f.desc,
}


class BaseQueryParameters(object):

    def from_request(self, request):
        args = request.args.copy()
        fields = request.args.get('fields', [])
        sort = request.args.get('sort', [])
        page = request.args.pop('page', 1)
        page_size = request.args.pop('page_size', 100)
        include = request.args.pop('include', [])


def parse_param(key, value):
    key, op = (key.rsplit(':', 1) + ['eq'])[:2]
    if key not in _keywords:
        value = [(op, v) for v in value]
    if key == 'sort':
        if op not in SORT_ORDER.keys():
            op = 'asc'
        value = [(op, v) for v in value]
    return key, value


def get_params():
    params = {}
    for key, value in request.args.iterlists():
        k, v = parse_param(key, value)
        params.setdefault(k, []).extend(v)
    return params
