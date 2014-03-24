# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, current_app
from nbs.models import db, Document, SaleInvoice
from nbs.models.document import TYPE_DOCUMENTS
from nbs.lib import rest
from nbs.utils import jsonify_form, jsonify_status_code
from nbs.forms import DocumentForm

document_api = Blueprint('api.document', __name__, url_prefix='/api/documents')

_spec = {
    'map': {},
    'required': ['id'],
    'defaults': ['id', 'issue_date'],
    'authorized': [],
}

@document_api.route('/types', methods=['GET'])
def list_doctypes():
    """Returns a list of available document types."""
    params = rest.get_params()
    result = rest.build_result_page(params, TYPE_DOCUMENTS)
    return jsonify(result)

@document_api.route('', methods=['GET'])
def list():
    """Returns a paginated list of documents."""
    params = rest.get_params(_spec)
    query = rest.get_query(Document, params)
    result = rest.get_result(query, params)
    return jsonify(result)

@document_api.route('/<int:id>', methods=['GET'])
def get(id):
    """Returns an individual document given an id."""
    params = rest.get_params(_spec)
    obj = Document.query.get_or_404(id)
    filtered = rest.filter_fields(obj.query, params)
    return jsonify(rest.to_dict(obj, filtered))

@document_api.route('', methods=['POST'])
def add():
    # read parameters from body request
    form = DocumentForm(csrf_enabled=False)
    if form.validate_on_submit():
        obj = rest.get_instance(Document, form.patch_data)
        try:
            db.session.add(obj)
            db.session.commit()
            return jsonify_status_code(201, **rest.to_dict(obj))
        except Exception as e:
            current_app.logger.exception(e.message)
            return rest.rest_abort(409, message='Confilict')
    return jsonify_form(form)
