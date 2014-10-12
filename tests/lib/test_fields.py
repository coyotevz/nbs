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

class Mock(object):
    pass


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

    def test_formatting_field_none(self):
        obj = {}
        field = fields.FormattedString("/foo/{0[account_sid]}/{0[sid]}/")
        with pytest.raises(MarshallingException):
            field.output("foo", obj)

    def test_formatting_field_tuple(self):
        obj = (3, 4)
        field = fields.FormattedString("/foo/{0[account_sid]}/{0[sid]}/")
        with pytest.raises(MarshallingException):
            field.output("foo", obj)

    def test_formatting_fiel_dict(self):
        obj = {"sid": 3, "account_sid": 4}
        field = fields.FormattedString("/foo/{account_sid}/{sid}/")
        assert field.output("foo", obj) == "/foo/4/3/"

    def test_formating_field(self):
        obj = Mock()
        obj.sid = 3
        obj.account_sid = 4
        field = fields.FormattedString("/foo/{account_sid}/{sid}/")
        assert field.output("foo", obj) == "/foo/4/3/"

    def test_basic_field(self):
        obj = Mock()
        obj.foo = 3
        field = fields.Field()
        assert field.output("foo", obj) == 3

    def test_nested_field(self):
        foo = Mock()
        bar = Mock()
        bar.value = 3
        foo.bar = bar
        field = fields.Field()
        assert field.output("bar.value", foo) == 3

    def test_formatted_string_invalid_obj(self):
        field = fields.FormattedString("{hey}")
        with pytest.raises(MarshallingException):
            field.output("hey", None)

    def test_formatted_string(self):
        field = fields.FormattedString("{hey}")
        assert field.output("foo", Foo()) == "3"

    def test_string_with_attribute(self):
        field = fields.String(attribute="hey")
        assert field.output("foo", Foo()) == "3"

    def test_int(self):
        field = fields.Integer()
        assert field.output("hey", {"hey": 3}) == 3

    def test_int_default(self):
        field = fields.Integer(default=1)
        assert field.output("hey", {"hey": None}) == 1

    def test_no_int(self):
        field = fields.Integer()
        assert field.output("hey", {"hey": None}) == 0

    def test_get_value(self):
        assert fields.get_value("hey", {"hey": 3}) == 3

    def test_get_value_no_value(self):
        assert fields.get_value("hey", {"hey": None}) is None

    def test_get_value_obj(self):
        assert fields.get_value("hey", Foo()) == 3

    def test_list(self):
        obj = {'list': ['a', 'b', 'c']}
        field = fields.List(fields.String)
        assert field.output("list", obj) == ['a', 'b', 'c']

    def test_list_from_set(self):
        obj = {'list': set(['a', 'b', 'c'])}
        field = fields.List(fields.String)
        assert set(field.output("list", obj)) == set(['a', 'b', 'c'])

    def test_list_from_object(self):
        class SomeObject(object):
            def __init__(self, list):
                self.list = list
        obj = SomeObject(['a', 'b', 'c'])
        field = fields.List(fields.String)
        assert field.output('list', obj) == ['a', 'b', 'c']






    #def test_function_field(self):
    #    field = fields.Function(lambda obj: obj.name.upper())
    #    assert "FOO" == field.output("key", self.user)

    #def test_function_with_uncallable_param(self):
    #    with pytest.raises(ValueError):
    #        fields.Function("uncallable")
