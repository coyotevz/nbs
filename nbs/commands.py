# -*- coding: utf-8 -*-

"""
    nbs.commands
    ~~~~~~~~~~~~

"""

from flask import current_app
from flask.ext.script import Manager, Shell, prompt_bool

from nbs import create_app
from nbs.models import db

manager = Manager(create_app)

@manager.command
def initdb(create_admin_user=True):
    """Creates database tables"""
    db.create_all()
    from nbs.models.product import create_primitive_units
    create_primitive_units()
    if create_admin_user:
        from nbs.models.user import create_admin_user
        create_admin_user()

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

def main():
    manager.run()

manager.add_command("shell", Shell(make_context=shell_make_context))
manager.add_option('-c', '--config', dest='config', required=False,
                   help='config file')
