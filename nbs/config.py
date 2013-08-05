# -*- coding: utf-8 -*-

from os import path, pardir

basedir = path.abspath(path.join(path.dirname(__file__), pardir))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<must be secret>' # use os.random(24) to generate this
    CRSF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'data.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
