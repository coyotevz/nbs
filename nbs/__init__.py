# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')

from flask import Flask, request
from nbs.models import configure_db
from nbs.auth import configure_auth
from nbs.api import configure_api
from nbs.views import configure_views

DEFAULT_APPNAME = 'nbs'


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name)

    configure_app(app, config)
    configure_db(app)
    configure_auth(app)
    configure_api(app)
    configure_views(app)

    return app


def configure_app(app, config=None):


    if config is not None:
        app.config.from_object(config)
    else:
        app.config.from_object('nbs.config.DevelopmentConfig')

    @app.route('/urls')
    def show_urls():
        from flask import escape
        return '<pre>'+str(escape(str(app.url_map)))+'</pre>'

    @app.before_request
    def set_page_params():
        max_per_page = app.config.get('MAX_ITEMS_PER_PAGE', 100)
        request.page = int(request.args.get('page', 1))
        request.per_page = min(int(request.args.get('per_page', 25)),
                               max_per_page)
