# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, json, current_app
from werkzeug.datastructures import MultiDict
from nbs.models import db, Product, ProductSupplierInfo, Warehouse
from nbs.auth import Need, Permission, permission_required
from nbs.lib import rest
from nbs.utils import is_json, jsonify_status_code, jsonify_form
from nbs.forms import ProductForm, ProductSupplierInfoForm

product_api = Blueprint('api.product', __name__, url_prefix='/api/products')

list_products_permission   = Permission(Need('list',    'product'))
get_products_permission    = Permission(Need('get',     'product'))
add_products_permission    = Permission(Need('add',     'product'))
update_products_permission = Permission(Need('update',  'product'))
delete_products_permission = Permission(Need('delete',  'product'))

# fields permissions
def build_fields_permissions(model):
    perms = []
    tname = model.__tablename__
    for col in rest.get_columns(model):
        perms.append(Permission(Need('read',  '{0}.{1}'.format(tname, col))))
        perms.append(Permission(Need('write', '{0}.{1}'.format(tname, col))))
    return perms

read_cost_permission   = Permission(Need('read',  'product.cost'))
write_cost_permission  = Permission(Need('write', 'product.cost'))
read_price_permission  = Permission(Need('read',  'product.price'))
write_price_permission = Permission(Need('write', 'product.price'))

def get_stocks(product):
    return product.get_stock_items()

def get_local_stock(product):
    # FIXME: Fake warehouse id, this must be fetched from session data
    wid = 8
    warehouse = Warehouse.query.get(wid)
    return product.get_stock_for_warehouse(warehouse, False)


_spec = {
    'map': {
        'stock': get_local_stock,
        'stocks': get_stocks,
    },
    'required': ['id', 'sku'],
    'defaults': ['id', 'sku', 'description', 'price'],
    'authorized': [],
}

_spec_ind = _spec.copy()
_spec_ind['defaults'] = _spec['defaults'] + ['stock']

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
    params = rest.get_params(_spec_ind)
    obj = Product.query.get_or_404(id)
    filtered = rest.filter_fields(obj.query, params)
    return jsonify(rest.to_dict(obj, filtered))

@product_api.route('', methods=['POST'])
def add():
    # read parameters for the model from the body of the request
    form = ProductForm(csrf_enabled=False)
    if form.validate_on_submit():
        obj = rest.get_instance(Product, form.patch_data)
        try:
            db.session.add(obj)
            db.session.commit()
            return jsonify_status_code(201, **rest.to_dict(obj))
        except Exception, e:
            current_app.logger.exception(e.message)
            return rest.rest_abort(409, message='Conflict')
    return jsonify_form(form)

@product_api.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product, csrf_enabled=False)
    if form.validate_on_submit():
        form.patch_obj(product)
        try:
            db.session.commit()
            return jsonify_status_code(201, **rest.to_dict(product))
        except Exception, e:
            current_app.logger.exception(e.message)
            return rest.rest_abort(409, message='Conflict')
    return jsonify_form(form)


## ProductSupplierInfo interface ##

@product_api.route('/<int:id>/supplierinfo', methods=['POST'])
def add_supplier_info(id):
    product = Product.query.get_or_404(id)
    form = ProductSupplierInfoForm(product_id=product.id, csrf_enabled=False)
    if form.validate_on_submit():
        data = dict(form.patch_data, product_id=product.id)
        print "data:", data
        obj = rest.get_instance(ProductSupplierInfo, data)
        try:
            db.session.add(obj)
            db.session.commit()
            return jsonify_status_code(201, **rest.to_dict(obj))
        except Exception, e:
            current_app.logger.exception(e.message)
            return rest.rest_abort(409, message='Conflict')
    return jsonify_form(form)

## PriceHistory getter ##

@product_api.route('/<int:id>/pricehistory', methods=['GET'])
def list_price_history(id):
    """Returns price history data for this product"""
    product = Product.query.get_or_404(id)
    result = [rest.to_dict(h, ['date', 'price']) for h in product.price_history]
    return jsonify({'price_history': result})
