# -*- coding: utf-8 -*-

from flask import Blueprint
from .jinjafilters import configure_jinja
from .views import dashboard, product, supplier, pos, admin

# Only holds static and templates folders
web = Blueprint('web', __name__,
                static_folder='static',
                template_folder='templates')

def configure_web(app):
    configure_jinja(app)
    app.register_blueprint(web)
    app.register_blueprint(dashboard)
    app.register_blueprint(product)
    app.register_blueprint(supplier)
    app.register_blueprint(pos)
    app.register_blueprint(admin)
