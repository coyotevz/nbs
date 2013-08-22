# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from nbs.models import db, Product
from nbs.forms import ProductForm

product = Blueprint('web.product', __name__, url_prefix='/product')


@product.route('/')
def list():
    products = Product.query.order_by(Product.sku).all()
    return render_template('product/list.html', products=products)

@product.route('/<id>')
def view(id):
    product = Product.query.get_or_404(id)
    return render_template('product/view.html', product=product)

@product.route('/new/')
def new():
    form = ProductForm()
    return render_template('product/new.html', form=form)
