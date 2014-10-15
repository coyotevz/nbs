# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, subqueryload
from webargs.flaskparser import FlaskParser

from nbs.models import db, Product, ProductStock
from nbs.lib import fields, marshal, args


## MARSHAL FIELDS ##

product_fields = {
    'id': fields.Integer,
    'sku': fields.String,
    'description': fields.String,
    'price': fields.Price,
}

warehouse_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

stock_fields = {
    'quantity': fields.Number,
    'warehouse': fields.Nested(warehouse_fields),
    'modified': fields.DateTime,
}

product_with_stock_fields = {
    'id': fields.Integer,
    'stock': fields.List(fields.Nested(stock_fields)),
}

supplier_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'fancy_name': fields.String,
}

supplier_info_fields = {
    'supplier': fields.Nested(supplier_fields),
    'sku': fields.String,
    'description': fields.String,
    'cost': fields.Price,
    'last_update': fields.DateTime,
}


## ARGS ##

parser = FlaskParser()

product_list_args = {
    'fields': args.FieldsArg(default=['id', 'sku', 'description', 'price']),
    'filters': args.QueryArg(),
}

## API ##

product_api = Blueprint('api.product', __name__, url_prefix='/api/products')

@product_api.route('', methods=['GET'])
@parser.use_kwargs(product_list_args)
def list(filters, fields):
    products = fields.apply_query(Product.query)
    return jsonify({"products": marshal(products, product_fields, many=True)})

@product_api.route('/<int:pk>', methods=['GET'])
def get(pk):
    product = Product.query.get(pk)
    if not product:
        return jsonify({"message": "Product could not be found."}), 404
    return jsonify(marshal(product, product_fields))

@product_api.route('/<list(int):pks>', methods=['GET'])
def get_many(pks):
    products = Product.query.filter(Product.id.in_(pks))
    return jsonify({"products": marshal(products, product_fields, many=True)})

@product_api.route('/<int:pk>/stocks', methods=['GET'])
def get_stock(pk):
    product = Product.query.get(pk)
    if not product:
        return jsonify({"message": "Product could not be found."}), 404
    return jsonify({
        "id": product.id,
        "stocks": marshal(product.stock, stock_fields, many=True),
    })

@product_api.route('/<list(int):pks>/stocks', methods=['GET'])
def get_many_stocks(pks):
    products = Product.query.filter(Product.id.in_(pks)).options(
        joinedload(Product.stock).joinedload(ProductStock.warehouse)
    )
    return jsonify({
        "products": marshal(products, product_with_stock_fields, many=True)
    })

@product_api.route('/<int:pk>/suppliers', methods=['GET'])
def get_suppliers_info(pk):
    product = Product.query.get(pk)
    if not product:
        return jsonify({"message": "Product could not be found."}), 404
    return jsonify({
        "id": product.id,
        "suppliers_info": marshal(product.suppliers_info,
                                  supplier_info_fields, many=True),
    })
