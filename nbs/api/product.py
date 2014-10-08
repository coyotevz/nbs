# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, subqueryload
from marshmallow import Serializer, fields

from nbs.models import db, Product, ProductStock


## SERIALIZERS ##

class ProductSerializer(Serializer):
    price = fields.Number()

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

## API ##

product_api = Blueprint('api.product', __name__, url_prefix='/api/products')

@product_api.route('', methods=['GET'])
def list():
    products = Product.query.all()
    return jsonify({"products": ProductSerializer(products, many=True).data})

@product_api.route('/<int:pk>', methods=['GET'])
def get(pk):
    try:
        product = Product.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Product could not be found."}), 400
    return jsonify(ProductSerializer(product).data)

@product_api.route('/<int:pk>/stocks', methods=['GET'])
def get_stock(pk):
    try:
        product = Product.query.get(pk)
    except IntegrityError:
        return jsonify({"message", "Product could not be found."}), 400
    return jsonify(ProductWithStockSerializer(product).data)

@product_api.route('/<list(int):pks>', methods=['GET'])
def get_many(pks):
    products = Product.query.filter(Product.id.in_(pks))
    return jsonify({"products": ProductSerializer(products, many=True).data})

@product_api.route('/<list(int):pks>/stocks', methods=['GET'])
def get_many_stocks(pks):
    products = Product.query.filter(Product.id.in_(pks)).options(
        joinedload(Product.stock).joinedload(ProductStock.warehouse)
    )
    return jsonify({"products": ProductWithStockSerializer(products, many=True).data})
