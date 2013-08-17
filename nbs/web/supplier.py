# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

from nbs.models import db, Supplier

supplier = Blueprint('web.supplier', __name__, url_prefix='/supplier')

@supplier.route('/')
def index():
    page = int(request.args.get('page', 1))
    suppliers = Supplier.query.order_by(Supplier.name)
    pagination = suppliers.paginate(page, per_page=40)
    return render_template('supplier/index.html', pagination=pagination)
