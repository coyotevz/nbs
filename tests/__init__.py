# -*- coding: utf-8 -*-

from nbs import create_app
from nbs.config import TestingConfig
from nbs.models import db

class TestCase(object):
    """Base class for test which use a Flask application

    The Flsak test client can be accesed at ``self.client``.  The Flask
    application itself is accesible at ``self.app``.
    """

    def setup(self):
        self.app = create_app(config=TestingConfig)
        self._app_context = self.app.app_context()
        self._app_context.push()
        self.client = self.app.test_client()

    def teardown(self):
        self._app_context.pop()
        self.app = None


class DBTestCase(TestCase):
    """Base class for test that involves database operations"""

    def setup(self):
        super(DBTestCase, self).setup()
        self.db = db
        self.db.create_all()

    def teardown(self):
        self.db.drop_all()
        super(DBTestCase, self).teardown()
