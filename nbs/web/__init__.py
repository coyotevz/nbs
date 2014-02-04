# -*- coding: utf-8 -*-

from .jinjafilters import configure_jinja
from .views import web

def configure_web(app):
    configure_jinja(app)
    app.register_blueprint(web)
