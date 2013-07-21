# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, json, current_app
from nbs.models import db, Product
from nbs.auth import Need, Permission, permission_required
from nbs.lib import rest
from nbs.utils import is_json, jsonify_status_code

product_api = Blueprint('api.product', __name__, url_prefix='/api/product')

list_products_permission   = Permission(Need('list',    'product'))
get_products_permission    = Permission(Need('get',     'product'))
add_products_permission    = Permission(Need('add',     'product'))
update_products_permission = Permission(Need('update',  'product'))
delete_products_permission = Permission(Need('delete',  'product'))

# fields permissions
read_cost_permission   = Permission(Need('read',  'product.cost'))
write_cost_permission  = Permission(Need('write', 'product.cost'))
read_price_permission  = Permission(Need('read',  'product.price'))
write_price_permission = Permission(Need('write', 'product.price'))

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
    obj = rest.get_instance(Product, data)
    try:
        db.session.add(obj)
        db.session.commit()
        return jsonify_status_code(201, **rest.to_dict(obj))
    except:
        return rest.rest_abort(409, message='Conflict')
