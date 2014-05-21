# -*- coding: utf-8 -*-

"""
    nbs.lib.rest
    ~~~~~~~~~~~~

    Provides tools for building REST interfaces.
"""

import datetime
import uuid
import decimal
from collections import namedtuple

from sqlalchemy import and_
from sqlalchemy.orm import (
    ColumnProperty, SynonymProperty, RelationshipProperty, object_mapper
)
from sqlalchemy.orm.util import class_mapper
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.exceptions import default_exceptions, HTTPException
from flask import request, make_response, abort, json, current_app
from flask.ext.sqlalchemy import Pagination

from nbs.utils import is_json

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
                 sort=None, single=False, spec=None):
        self.fields = fields or []
        self.filters = filters or []
        self.page = page or 1
        self.per_page = per_page or 25
        self.sort = sort or []
        self.single = bool(single)
        self.spec = spec

    def __repr__(self):
        template = ('<QueryParameters fields={}, filters={}, sort={}, '
                    'page={}, per_page={}, single={}>')
        return template.format(self.fields, self.filters, self.sort,
                               self.page, self.per_page, self.single)

    @staticmethod
    def from_dict(data, spec=None):
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
                               per_page=per_page, sort=sort, single=single,
                               spec=spec)


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
            fname = f.field
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


def get_params(spec=None):
    """
    Returns a QueryParameters instance for query string received.
    """
    params = {}
    for key, value in request.args.iterlists():
        k, v = parse_param(key, value)
        params.setdefault(k, []).extend(v)
    unroll_params(params)
    return QueryParameters.from_dict(params, spec)


# From old module
class RestException(HTTPException):

    def __init__(self, message, code=None):
        HTTPException.__init__(self, message)
        if code is not None:
            self.code = code

    def get_body(self, environ):
        return json.dumps({
            'code': self.code,
            'message': self.description,
        })

    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]

def rest_abort(code=400, message=None):
    bases = [RestException]
    if code in default_exceptions:
        bases.insert(0, default_exceptions[code])
    error = type('RestException', tuple(bases), dict(code=code))(message)
    abort(make_response(error, code, {}))

def get_data():
    if not is_json(request):
        msg = u'Request must have "Content-Type: application/json" header'
        rest_abort(415, message=msg)

    try:
        params = json.loads(request.data)
    except (TypeError, ValueError, OverflowError) as exception:
        current_app.logger.exception(exception.message)
        rest_abort(400, message=u'Unable to decode data')

    return params

def get_to_update(model, params):
    cols = get_columns(model)
    for field in params:
        if field not in cols:
            msg = "Model '%s' does not have field '%s'" % (model.__name__,
                                                           field)
            rest_abort(400, message=msg)

    props = set(cols).intersection(params.keys())
    return dict((p, params[p]) for p in props)

def get_query(model, params):
    return SQLQueryBuilder.create_query(model, params)

def filter_fields(query, params):
    fields = build_fields_spec(params)

    # retrieve available columns for model involved in query
    model = query.column_descriptions[0]['type']
    columns = get_columns(model)
    columns = set(columns + fields.get('map', {}).keys())


    if fields['requested']:
        requested = set(fields['requested'])
    else:
        if (len(fields['defaults']) == 1 and fields['defaults'][0] == u'*') or\
            len(fields['defaults']) == 0:
            requested = set(columns)
        else:
            requested = set(fields['defaults'])

    required = set(fields['required'])

    requested.intersection_update(columns)
    requested.update(required)

    # TODO: Work with authorized fields

    for key, value in fields['map'].iteritems():
        if key in requested:
            requested.remove(key)
            requested.add((key, value))

    return list(requested)


def build_fields_spec(params):
    fields = {'requested': params.fields}
    if params.spec:
        fields.update({
            'defaults': params.spec.get('defaults', []),
            'required': params.spec.get('required', []),
            'authorized': params.spec.get('authorized', []),
            'map': params.spec.get('map', {}),
        })
    return fields

def get_result(query, params):
    filtered = filter_fields(query, params)
    result = query.paginate(params.page, params.per_page)
    return {
        'num_results': result.total,
        'page': result.page,
        'num_pages': result.pages,
        'objects': [to_dict(i, filtered) for i in result.items],
    }

def _getcol(obj, column):
    if hasattr(obj, "{}_str".format(column)):
        return getattr(obj, "{}_str".format(column))
    return getattr(obj, column)

def to_dict(obj, fields=None, extra=None, exclude=None):

    if fields is None:
        fields = get_columns(object_mapper(obj).class_)

    fields = set(fields)

    if extra is not None:
        if isinstance(extra, (list, tuple)):
            extra = list(extra)
        elif isinstance(extra, basestring):
            extra = [extra]
        else:
            raise TypeError("extra= argument of to_dict() must be an iterable "
                            "or string")
        fields = fields.union(set(extra))

    if exclude is not None:
        if isinstance(exclude, (list, tuple)):
            exclude = list(exclude)
        elif isinstance(exclude, basestring):
            exclude = [exclude]
        else:
            raise TypeError("exclude= argument of to_dict() must be an "
                            "iterable or string")
        fields = fields - set(exclude)

    result = dict((col, _getcol(obj, col)) for col in fields\
                  if isinstance(col, basestring))

    result.update(dict((m[0], m[1](obj)) for m in fields\
                  if isinstance(m, tuple)))

    # Check for objects in the dictionary that may not be serializable by
    # default. Specifically, convert datetime and date objects to ISO8601
    # format, UUID objects to exadecimal and Decimal objects to string.
    for key, value in result.items():
        result[key] = _clean(value)

    return result

def _clean(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, (uuid.UUID, decimal.Decimal)):
        return str(value)
    elif is_mapped_class(type(value)):
        return to_dict(value)
    elif isinstance(value, dict):
        return {k: _clean(v) for k, v in value.iteritems()}
    elif isinstance(value, list):
        return [_clean(v) for v in value]
    return value

def get_columns(model):
    columns = [p.key for p in class_mapper(model).iterate_properties
               if isinstance(p, (ColumnProperty, SynonymProperty)) \
                  and not p.key.startswith('_')]
    for parent in model.mro():
        columns += [key for key, value in parent.__dict__.iteritems()
                    if isinstance(value, hybrid_property)]
    return columns


def get_required_columns(model):
    return [c.key for c in class_mapper(model).columns if \
            ((c.nullable is False) and (c.primary_key is False))]


def get_instance(model, data):
    cols = get_to_update(model, data)
    required = set(get_required_columns(model))
    if required.intersection(cols.keys()) != required:
        msg = "Missing fields for model '%s'" % (model.__name__,)
        rest_abort(400, message=msg)
    return model(**cols)


def get_relations(model):
    return [p.key for p in class_mapper(model).iterate_properties
            if isinstance(p, RelationshipProperty)]


def is_mapped_class(cls):
    try:
        class_mapper(cls)
        return True
    except:
        return False


def to_dict_list_getter(field_name, fields=None):
    def getter(obj):
        return [to_dict(f, fields) for f in getattr(obj, field_name)]
    return getter


def build_result_page(params, items):
    result = Pagination(None, params.page, params.per_page, len(items), items)
    return {
        'num_result': result.total,
        'page': result.page,
        'num_pages': result.pages,
        'objects': result.items,
    }
