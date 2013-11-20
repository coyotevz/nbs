# -*- coding: utf-8 -*-

"""
    nbs.commands
    ~~~~~~~~~~~~

"""

import sys
from flask import current_app
from flask.ext.script import Manager, Shell, prompt_bool
from flask.ext.script import Command, Option

from nbs import create_app
from nbs.models import db

manager = Manager(create_app)

@manager.command
def initdb(create_admin_user=True, with_fixtures=False):
    """Creates database tables"""
    db.create_all()
    from nbs.models.product import create_primitive_units
    create_primitive_units()
    if create_admin_user:
        from nbs.models.user import create_admin_user
        create_admin_user()
    if with_fixtures:
        from nbs.sample_data import install_fixtures
        install_fixtures()

@manager.command
def dropdb():
    """Drops all database tables"""
    if prompt_bool("Are you sure ? You will lose all your data!"):
        db.drop_all()

def shell_make_context():
    from datetime import datetime
    from decimal import Decimal
    return dict(
        app=current_app,
        db=db,
        Decimal=Decimal,
        datetime=datetime
    )

manager.add_command("shell", Shell(make_context=shell_make_context))

class GunicornServer(Command):

    description = u'Run the app within Gunicorn'

    def __init__(self, host='127.0.0.1', port=8000, workers=4):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-H', '--host', dest='host', default=self.host),
            Option('-p', '--port', dest='port', default=self.port),
            Option('-w', '--workers', dest='workers', default=self.workers),
        )

    def handle(self, app, host, port, workers):
        from gunicorn import version_info

        if version_info < (0, 9, 0):
            print "We can't run this yet"
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, options, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers,
                    }

                def load(self):
                    return app

            FlaskApplication().run()

manager.add_command("gunicorn", GunicornServer())


class PyTest(Command):

    description = u'Run py.test over the entire project'

    def handle(self, app):
        import pytest
        errno = pytest.main(sys.argv[2:])
        sys.exit(errno)

manager.add_command("test", PyTest())

def main():
    manager.run()

