# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')

from flask import Flask, request
from flask import Request as _Request
from werkzeug.datastructures import ImmutableOrderedMultiDict

from nbs.models import configure_db
from nbs.auth import configure_auth
from nbs.api import configure_api
from nbs.web import configure_web

DEFAULT_APPNAME = 'nbs'


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name, static_folder=None)

    configure_app(app, config)
    configure_db(app)
    configure_auth(app)
    configure_api(app)
    configure_web(app)

    return app


class Request(_Request):
    """Redefine Request that uses ImmutableOrderedMultiDict for .args"""
    parameter_storage_class = ImmutableOrderedMultiDict

def run_scss(app):
    import subprocess, atexit

    infile = '%s/web/static/scss/nobix.scss' % app.root_path
    outfile = '%s/web/static/css/nobix.css' % app.root_path

    proc = subprocess.Popen(['/usr/bin/scss', '--watch', '%s:%s' % (infile, outfile)])
    atexit.register(proc.kill)

def is_running_main():
    import os
    return os.environ.get('WERKZEUG_RUN_MAIN', False)

def configure_app(app, config=None):

    # Set custom Request class
    app.request_class = Request

    if config is not None:
        app.config.from_object(config)
    else:
        app.config.from_object('nbs.config.DevelopmentConfig')

    if app.debug and not is_running_main():
        run_scss(app)

    @app.before_request
    def set_page_params():
        max_per_page = app.config.get('MAX_ITEMS_PER_PAGE', 100)
        request.page = int(request.args.get('page', 1))
        request.per_page = min(int(request.args.get('per_page', 25)),
                               max_per_page)
