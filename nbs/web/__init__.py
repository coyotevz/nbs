# -*- coding: utf-8 -*-

from .product import product
from .supplier import supplier

def configure_web(app):
    app.register_blueprint(product)
    app.register_blueprint(supplier)
