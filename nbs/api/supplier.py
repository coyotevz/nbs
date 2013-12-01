# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from nbs.models import Supplier, Contact
from nbs.auth import Need, Permission, permission_required
from nbs.lib import rest

supplier_api = Blueprint('api.supplier', __name__, url_prefix='/api/suppliers')

list_suppliers_permission   = Permission(Need('list',   'supplier'))
get_suppliers_permission    = Permission(Need('get',    'supplier'))
add_suppliers_permission    = Permission(Need('add',    'supplier'))
update_suppliers_permission = Permission(Need('update', 'supplier'))
delete_suppliers_permission = Permission(Need('delete', 'supplier'))

_cf = ['id', 'full_name', 'notes']
def _supplier_contacts(supplier, fields=None):
    return [dict(rest.to_dict(sc.contact, fields or _cf).items() +
                 [('role', sc.role)]) for sc in supplier.supplier_contacts]

def _supplier_products(supplier, fields=None):
    # TODO: Complete this function
    return []

_supplier_relations_map = {
    'contacts': _supplier_contacts,
    'products': _supplier_products,
}

_spec = {
    'map': _supplier_relations_map,
    'required': ['id'],
    'defaults': ['id', 'cuit', 'name', 'fancy_name', 'payment_term',
                'notes', 'contacts'],
    'authorized': [],
}

@supplier_api.route('', methods=['GET'])
@permission_required(list_suppliers_permission)
def list():
    """Returns a paginated list of suppliers that match with the given
    conditions.
    """
    params = rest.get_params(_spec)
    query = rest.get_query(Supplier, params)
    result = rest.get_result(query, params)
    return jsonify(result)

@supplier_api.route('/<int:id>', methods=['GET'])
@permission_required(get_suppliers_permission)
def get(id):
    """Returns an individual supplier given an id"""
    params = rest.get_params(_spec)
    obj = Supplier.query.get_or_404(id)
    filtered = rest.filter_fields(obj.query, params)
    return jsonify(rest.to_dict(obj, filtered))

@supplier_api.route('', methods=['POST'])
@permission_required(add_suppliers_permission)
def add():
    return 'POST'

@supplier_api.route('/<int:id>', methods=['PUT', 'PUSH'])
@permission_required(update_suppliers_permission)
def update(id):
    return 'PUT {0}'.format(id)

@supplier_api.route('/<int:id>', methods=['DELETE'])
@permission_required(delete_suppliers_permission)
def delete(id):
    return 'DELTE {0}'.format(id)

# Aditional methods
_scontact_fields = rest.get_columns(Contact) + [
    ('address', rest.to_dict_list_getter('address')),
    ('phone', rest.to_dict_list_getter('phone')),
    ('email', rest.to_dict_list_getter('email')),
    ('extra_field', rest.to_dict_list_getter('extra_field')),
]

@supplier_api.route('/<int:id>/contacts', methods=['GET'])
def list_contacts(id):
    """Returns a paginated list of contacts associated with given supplier"""
    params = rest.get_params()
    supplier = Supplier.query.get_or_404(id)
    items = _supplier_contacts(supplier, _scontact_fields)
    result = rest.build_result_page(params, items)
    return jsonify(result)

_product_fields = []
@supplier_api.route('/<int:id>/products', methods=['GET'])
def list_products(id):
    """Returns a paginated list of products associated with given supplier"""
    params = rest.get_params()
    supplier = Supplier.query.get_or_404(id)
    items = _supplier_products(supplier, _product_fields)
    result = rest.build_result_page(params, items)
    return jsonify(result)
