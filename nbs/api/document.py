# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from nbs.models import db, Document, SaleInvoice
from nbs.lib import rest

document_api = Blueprint('api.document', __name__, url_prefix='/api/documents')

_spec = {
    'map': {},
    'required': ['id'],
    'defaults': ['id', 'issue_date'],
    'authorized': [],
}

@document_api.route('', methods=['GET'])
def list():
    """Returns a paginated list of documents."""
    params = rest.get_params(_spec)
    query = rest.get_query(Document, params)
    result = rest.get_result(query, params)
    return jsonify(result)
