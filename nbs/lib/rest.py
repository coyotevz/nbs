# -*- coding: utf-8 -*-

"""
    nbs.lib.rest
    ~~~~~~~~~~~~

    Provides tools for building REST interfaces.
"""

import inspect
import datetime
import uuid

from flask import Blueprint, request, current_app, json, make_response, abort
from flask.ext.sqlalchemy import Pagination

from werkzeug.exceptions import default_exceptions, HTTPException

from sqlalchemy import and_ as AND, or_ as OR
from sqlalchemy.orm import ColumnProperty, RelationshipProperty, object_mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.util import class_mapper
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.ext.hybrid import hybrid_property

from nbs.utils import is_json


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

def _sub_operator(model, argument, fieldname):
    if isinstance(model, InstrumentedAttribute):
        submodel = model.property.mapper.class_
    elif isinstance(model, AssociationProxy):
        submodel = get_related_association_proxy_model(model)
    else:
        pass
    if isinstance(argument, dict):
        fieldname = argument['name']
        operator = argument['op']
        argument = argument['val']
        relation = None
        if '.' in fieldname:
            fielname, relation = fieldname.split('.')
        return create_operation(submodel, fieldname, operator,
                                argument, relation)

    return getattr(submodel, fieldname) == argument

OPERATORS = {
    # Operators which accept a single argument.
    'is_null': lambda f: f == None,
    'is_not_null': lambda f: f != None,
    'desc': lambda f: f.desc,
    'asc': lambda f: f.asc,
    # Operators which accepts two arguments.
    '==': lambda f, a: f == a,
    'eq': lambda f, a: f == a,
    'equals': lambda f, a: f == a,
    'equal_to': lambda f, a: f == a,
    '!=': lambda f, a: f != a,
    'ne': lambda f, a: f != a,
    'neq': lambda f, a: f != a,
    'not_equal_to': lambda f, a: f != a,
    'does_not_equal': lambda f, a: f != a,
    '>': lambda f, a: f > a,
    'gt': lambda f, a: f > a,
    '<': lambda f, a, : f < a,
    'lt': lambda f, a: f < a,
    '>=': lambda f, a: f >= a,
    'ge': lambda f, a: f >= a,
    'gte': lambda f, a: f >= a,
    '<=': lambda f, a: f <= a,
    'le': lambda f, a: f <= a,
    'lte': lambda f, a: f <= a,
    'ilike': lambda f, a: f.ilike(a),
    'like': lambda f, a: f.like(a),
    'in': lambda f, a: f.in_(a),
    'not_in': lambda f, a: ~f.in_(a),
    # Operators which accpets three arguments.
    'has': lambda f, a, fn: f.has(_sub_operator(f, a, fn)),
    'any': lambda f, a, fn: f.any(_sub_operator(f, a, fn)),
}


class OrderBy(object):
    """Represents an "order by" in SQL query expression."""

    def __init__(self, field, direction='asc'):
        self.field = field
        self.direction = direction

    def __repr__(self):
        return '<OrderBy {}, {}>'.format(self.field, self.direction)


class Filter(object):
    """Represents a filter to apply to a SQL query."""

    def __init__(self, fieldname, operator, argument=None, otherfield=None):
        self.fieldname = fieldname
        self.operator = operator
        self.argument = argument
        self.otherfield = otherfield

    def __repr__(self):
        return '<Filter {} {} {}>'.format(self.fieldname, self.operator,
                                          self.argument or self.otherfield)

    @staticmethod
    def from_dict(data):
        """Returns a new :class:`Filter` object with arguments parsed from
        `data`.

        `data` is a data of the form::
            
            {'name': 'age', 'op': 'lt', 'val': 20}

        or::

            {'name': 'age', 'op': 'lt', 'field': 'height'}
        
        """
        fieldname = data.get('name')
        operator = data.get('op')
        argument = data.get('val')
        otherfield = data.get('field')
        return Filter(fieldname, operator, argument, otherfield)


class QueryParameters(object):
    """Aggregates the parameter for a search, including filters, search type,
    page, per_page, order by directive and fields to retrieve from.
    """

    def __init__(self, fields=None, filters=None, page=None, per_page=None,
                 order_by=None, junction=None, single=False, spec=None):
        self.fields = fields or []
        self.filters = filters or []
        self.page = page or 1
        self.per_page = per_page or 25
        self.order_by = order_by or []
        self.junction = junction or AND
        self.single = bool(single)
        self.spec = spec

    def __repr__(self):
        template = ('<QueryParameters fields={}, filters={}, order_by={}, '
                    'page={}, per_page={}, junction={}, single={}>')
        return template.format(self.fields, self.filters, self.order_by,
                               self.page, self.per_page,
                               self.junction.__name__, self.single)

    @staticmethod
    def from_dict(data, spec=None):
        """Returns a new :class:`Parameters` object with arguments parsed from
        `data`.

        `data` is of the form::

            {
                'filters': [{'name': 'age', 'op': 'lt', 'val': 20}, ...],
                'order_by': [{'field': 'age', 'direction': 'desc'}, ...],
                'page': 2,
                'per_page': 20,
                'disjuction': True,
                'single': True,
                'fields': ['name', 'age', 'height'],
            }
        """
        fields = data.get('fields', [])
        filters = [Filter.from_dict(f) for f in data.get('filters',  [])]
        order_by = [OrderBy(**o) for o in data.get('order_by', [])]
        page = data.get('page')
        per_page = data.get('per_page')
        junction = OR if data.get('disjuction') else AND
        single = data.get('single', False)
        return QueryParameters(fields=fields, filters=filters, page=page,
                               per_page=per_page, order_by=order_by,
                               junction=junction, single=single, spec=spec)


class SQLQueryBuilder(object):
    """Provides static functions for building a SQLAlchemy query object based
    on a :class:`QueryParameters` instance.
    """

    @staticmethod
    def create_operation(model, fieldname, operator, argument, relation=None):
        """Translates an operation described as string to a valid SQLAlchemy
        query parameter using a field or relation of the model.
        """

        opfunc = OPERATORS[operator]
        argspec = inspect.getargspec(opfunc)
        numargs = len(argspec.args)
        field = getattr(model, relation or fieldname)
        if numargs == 1:
            return opfunc(field)
        if argument is None:
            raise TypeError
        if numargs == 2:
            return opfunc(field, argument)
        return opfunc(field, argument, fieldname)


    @staticmethod
    def create_filters(model, query_params):
        """Returns a list of operations on `model` specified in the
        :attr:`filters` attribute on the `query_params` object.
        """
        filters = []
        for f in query_params.filters:
            fname = f.fieldname
            val = f.argument
            relation = None
            if '.' in fname:
                relation, fname = fname.split('.')
            if f.otherfield:
                val = getattr(model, f.otherfield)
            param = SQLQueryBuilder.create_operation(model, fname, f.operator,
                                                     val, relation)
            filters.append(param)

        return filters

    @staticmethod
    def create_query(model, query_params):

        if not isinstance(query_params, QueryParameters):
            raise ValueError("query_params must be an instance of "
                             "QueryParameters")

        # TODO: Optimize query based on relations required
        query = model.query

        # Adding field filters
        filters = SQLQueryBuilder.create_filters(model, query_params)
        query = query.filter(query_params.junction(*filters))

        # Order the search
        for val in query_params.order_by:
            field = getattr(model, val.field)
            direction = getattr(field, val.direction)
            query = query.order_by(direction())

        return query

def get_params(spec=None):
    try:
        params = json.loads(request.args.get('q', '{}'))
        params.setdefault('page', request.page)
        params.setdefault('per_page', request.per_page)
        return QueryParameters.from_dict(params, spec)
    except (TypeError, ValueError, OverflowError), exc:
        current_app.logger.exception(exc.message)
        rest_abort(400, message=u'Unable to decode data')

def get_data():
    if not is_json(request):
        msg = u'Request must have "Content-Type: application/json" header'
        rest_abort(415, message=msg)

    try:
        params = json.loads(request.data)
    except (TypeError, ValueError, OverflowError), exception:
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

def to_dict(obj, fields=None):

    if fields is None:
        fields = get_columns(object_mapper(obj).class_)

    result = dict((col, getattr(obj, col)) for col in fields\
                  if isinstance(col, basestring))

    result.update(dict((m[0], m[1](obj)) for m in fields\
                  if isinstance(m, tuple)))

    return result


def get_columns(model):
    columns = [p.key for p in class_mapper(model).iterate_properties
               if isinstance(p, ColumnProperty) and not p.key.startswith('_')]
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
