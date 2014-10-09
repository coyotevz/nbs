# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, subqueryload
from marshmallow import Serializer, fields

from nbs.models import db, Product, ProductStock


## SERIALIZERS ##

class ProductSerializer(Serializer):
    price = fields.Price()

    class Meta:
        fields = ("id", "sku", "description", "price")


class WarehouseSerializer(Serializer):

    class Meta:
        fields = ("id", "name")


class StockSerializer(Serializer):
    quantity = fields.Number()
    warehouse = fields.Nested(WarehouseSerializer)

    class Meta:
        fields = ("warehouse", "quantity", "modified")


class ProductWithStockSerializer(Serializer):
    stock = fields.Nested(StockSerializer, many=True)
    
    class Meta:
        fields = ("id", "stock")


class SupplierSerializer(Serializer):

    class Meta:
        fields = ("id", "name", "fancy_name")


class SupplierInfoSerializer(Serializer):
    supplier = fields.Nested(SupplierSerializer)
    cost = fields.Price()

    class Meta:
        fields = ("supplier", "sku", "description", "cost", "last_update")

## API ##

product_api = Blueprint('api.product', __name__, url_prefix='/api/products')

@product_api.route('', methods=['GET'])
def list():
    products = Product.query
    return jsonify({"products": ProductSerializer(products, many=True).data})

@product_api.route('/<int:pk>', methods=['GET'])
def get(pk):
    product = Product.query.get(pk)
    if not product:
        return jsonify({"message": "Product could not be found."}), 404
    return jsonify(ProductSerializer(product).data)

@product_api.route('/<list(int):pks>', methods=['GET'])
def get_many(pks):
    products = Product.query.filter(Product.id.in_(pks))
    return jsonify({"products": ProductSerializer(products, many=True).data})

@product_api.route('/<int:pk>/stocks', methods=['GET'])
def get_stock(pk):
    product = Product.query.get(pk)
    if not product:
        return jsonify({"message": "Product could not be found."}), 404
    return jsonify({
        "id": product.id,
        "stocks": StockSerializer(product.stock, many=True).data,
    })
    #return jsonify(ProductWithStockSerializer(product).data)

@product_api.route('/<list(int):pks>/stocks', methods=['GET'])
def get_many_stocks(pks):
    products = Product.query.filter(Product.id.in_(pks)).options(
        joinedload(Product.stock).joinedload(ProductStock.warehouse)
    )
    return jsonify({"products": ProductWithStockSerializer(products, many=True).data})

@product_api.route('/<int:pk>/suppliers', methods=['GET'])
def get_suppliers_info(pk):
    product = Product.query.get(pk)
    if not product:
        return jsonify({"message": "Product could not be found."}), 404
    return jsonify({
        "id": product.id,
        "suppliers_info": SupplierInfoSerializer(product.suppliers_info, many=True).data
    })
