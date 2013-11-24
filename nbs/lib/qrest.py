# -*- coding: utf-8 -*-

"""
    nbs.lib.rest
    ~~~~~~~~~~~~

    Provides tools for building REST interfaces.
"""

reserved_keywords = [
    'page', 'page_size', 'single', 'sort', 'fields', 'include'
]

OPERATORS = {

    # General comparators
    'eq': lambda f, a: f == a,
    'neq': lambda f, a: f != a,
    'gt': lambda f, a: f > a,
    'gte': lambda f, a: f => a,
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
    'ASC': lambda f: f.asc,
    'DESC': lambda f: f.desc,
}

def get_data():
    if not is_json(request):
        msg = u'Request must have "Content-Type: application/json" header'

    return request.args


class BaseQueryParameters(object):

    def from_request(self, request):
        # prefilter
        fields = request.args.get('fields', [])
        sort = request.args.get('sort', [])
        page = request.args.pop('page', 1)
        page_size = request.args.pop('page_size', 100)
        include = request.args.pop('include', [])
