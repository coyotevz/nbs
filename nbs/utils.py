# -*- coding: utf-8 -*-

import datetime
import uuid
import decimal
from flask import json, jsonify

def jsonify_status_code(status_code, headers=None, *args, **kwargs):
    """Returns a jsonified response with the specified HTTP status code.

    The positional and keyword arguments are passed directly to the
    :func:`flask.jsonify` function which creates the response.
    """

    for key, value in kwargs.items():
        if isinstance(value, datetime.date):
            kwrags[key] = value.isoformat()
        elif isinstance(value, (uuid.UUID, decimal.Decimal)):
            kwargs[key] = str(value)
        elif is_mapped_class(type(value)):
            kwargs[key] = to_dict(value)

    response = jsonify(*args, **kwargs)
    response.status_code = status_code
    if headers:
        for key, value in headers.iteritems():
            response.headers[key] = value
    return response

def jsonify_form(form):
    """Returns a json representation of WTForm instance.
    """
    has_errors = len(form.errors) > 0

    if has_errors:
        code = 400
        data = {'errors': form.errors}
    else:
        code = 200
        #data = {'form': form.data}
        data = form.patch_data

    if form.csrf_enabled and code == 200:
        data['form']['csrf_token'] = str(form.csrf_token.current_token)

    return jsonify_status_code(code, **data)

def is_json(req):
    return req.mimetype == 'application/json'

# circular dependencies
from nbs.lib.rest import is_mapped_class, to_dict
