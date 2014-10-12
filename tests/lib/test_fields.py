# -*- coding: utf-8 -*-

import datetime as dt
from collections import namedtuple
import pytest

from nbs.lib import fields, marshal, MarshallingException


class Foo(object):
    def __init__(self):
        self.hey = 3

class Bar(object):
    def __marshallable__(self):
        return {"hey": 3}


class TestFields(object):

    def test_repr(self):
        field = fields.String()
        assert repr(field) == "<String Field>"

    def test_basic_dictionary(self):
        obj = {"foo": 3}
        field = fields.String()
        assert field.output("foo", obj) == "3"

    def test_no_attribute(self):
        obj = {"bar": 3}
        field = fields.String()
        assert field.output("foo", obj) is None

    def test_date_field_invalid(self):
        obj = {"bar": 3}
        field = fields.DateTime()
        with pytest.raises(MarshallingException):
            field.output("bar", obj)

    def test_attribute(self):
        obj = {"bar": 3}
        field = fields.String(attribute="bar")
        assert field.output("foo", obj) == "3"

    #def test_function_field(self):
    #    field = fields.Function(lambda obj: obj.name.upper())
    #    assert "FOO" == field.output("key", self.user)

    #def test_function_with_uncallable_param(self):
    #    with pytest.raises(ValueError):
    #        fields.Function("uncallable")
