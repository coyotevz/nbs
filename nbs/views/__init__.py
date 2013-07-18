# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from .product import product
from .supplier import supplier

def configure_views(app):
    app.register_blueprint(product)
    app.register_blueprint(supplier)
