# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, json, current_app
from nbs.models import Product
from nbs.auth import Need, Permission, permission_required
from nbs.lib import rest
from nbs.utils import is_json, jsonify_status_code

product_api = Blueprint('api.product', __name__, url_prefix='/api/product')

_spec = {
    'map': {},
    'required': ['id', 'sku'],
    'defaults': ['id', 'sku', 'description', 'short_description', 'price'],
    'authorized': [],
}

@product_api.route('', methods=['GET'])
def list():
    """Returns a paginated list of products."""
    params = rest.get_params(_spec)
    query = rest.get_query(Product, params)
    result = rest.get_result(query, params)
    return jsonify(result)

@product_api.route('/<int:id>', methods=['GET'])
def get(id):
    """Returns an individual product given an id."""
    params = rest.get_params(_spec)
    obj = Product.query.get_or_404(id)
    filtered = rest.filter_fields(obj.query, params)
    return jsonify(rest.to_dict(obj, filtered))

@product_api.route('', methods=['POST'])
def add():
    # read parameters for the model from the body of the request
    data = rest.get_data()
    print data
    obj = rest.get_instance(Product, data)
    print obj
    return 'POST'
