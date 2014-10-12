# -*- coding: utf-8 -*-

from email.utils import formatdate
from calendar import timegm
import six

from nbs.lib import marshal, MarshallingException


def is_indexable_but_not_string(obj):
    return not hasattr(obj, "strip") and hasattr(obj, "__iter__")

def get_value(key, obj, default=None):
    if isinstance(key, int):
        return _get_value_for_key(key, obj, default)
    else:
        return _get_value_for_keys(key.split('.'), obj, default)

def _get_value_for_keys(keys, obj, default):
    if len(keys) == 1:
        return _get_value_for_key(keys[0], obj, default)
    else:
        return _get_value_for_keys(
            keys[1:], _get_value_for_key(keys[0], obj, default), default)

def _get_value_for_key(key, obj, default):
    if is_indexable_but_not_string(obj):
        try:
            return obj[key]
        except (IndexError, TypeError, KeyError):
            pass
    return getattr(obj, key, default)

def to_dict_like(obj):
    if obj is None:
        return None
    if hasattr(obj, '__getitem__'):
        return obj # it is indexable it is ok
    return dict(obj.__dict__)


class Field(object):
    """
    Basic field from which fields should extend. It applies no formatting by
    default, and should only be used in cases where data does not need to be
    formatted before being serialized.
    """

    _creation_index = 0

    def __init__(self, default=None, attribute=None):
        self.attribute = attribute
        self.default = default
        self._creation_index = Field._creation_index
        Field._creation_index += 1

    def format(self, value):
        """
        Formats a field's value. No-op by default - field classes that modify
        how the value of existing objects keys should be presented should
        override the and apply the appropriate formatting.
        """
        return value

    def output(self, key, obj):
        """
        Pulls the value for the given key from the object, applies the field's
        formatting and returns the result. If the key is not found in the
        object, return the default value. Field classes that create values
        which do not require the existence of the key in the object should
        override this and return the desired value.
        """
        value = get_value(key if self.attribute is None else self.attribute, obj)

        if value is None:
            return self.default

        return self.format(value)

    def __repr__(self):
        return '<{0} Field>'.format(self.__class__.__name__)


class Nested(Field):
    """
    Allows you to nest one set of fields inside another.
    """
    def __init__(self, nested, allow_null=False, **kwargs):
        self.nested = nested
        self.allow_null = allow_null
        super(Nested, self).__init__(**kwargs)

    def output(self, key, obj):
        value = get_value(key if self.attribute is None else self.attribute, obj)
        if self.allow_null and value is None:
            return None

        return marshal(value, self.nested)


class List(Field):
    """List of fields"""
    def __init__(self, cls_or_instance, **kwargs):
        super(List, self).__init__(**kwargs)
        error_msg = ("The type of the list elements must be a subclass of "
                     "lib.fields.Field")
        if isinstance(cls_or_instance, type):
            if not issubclass(cls_or_instance, Field):
                raise MarshallingException(error_msg)
            self.container = cls_or_instance()
        else:
            if not isinstance(cls_or_instance, Field):
                raise MarshallingException(error_msg)
            self.container = cls_or_instance

    def format(self, value):
        if isinstance(value, set):
            value = list(value)

        if is_indexable_but_not_string(value) and not isinstance(value, dict):
            return [self.container.output(idx, value) for idx in range(len(value))]
        if value is None:
            return self.default
        return [marshal(value, self.container.nested)]


class String(Field):

    def format(self, value):
        try:
            return six.text_type(value)
        except ValueError as ve:
            raise MarshallingException(ve)


class Integer(Field):
    """Field for outputting an integer value."""
    def __init__(self, default=0, attribute=None):
        super(Integer, self).__init__(default, attribute)

    def format(self, value):
        try:
            if value is None:
                return self.default
            return int(value)
        except ValueError as ve:
            raise MarshallingException(ve)


class Boolean(Field):

    def format(self, value):
        return bool(value)


class FormattedString(Field):
    """Interpolate other values from the object into this field. The syntax for
    the source strin gis the same as the string `str.format` method from python
    stdlib."""

    def __init__(self, src_str):
        super(FormattedString, self).__init__()
        self.src_str = six.text_type(src_str)

    def output(self, key, obj):
        try:
            data = to_dict_like(obj)
            return self.src_str.format(**data)
        except (TypeError, IndexError) as error:
            raise MarshallingException(error)


def isoformat(dt):
    return dt.isoformat()

def rfcformat(dt):
    return formatdate(timegm(dt.utctimetuple()))


DATEFORMAT_SERIALIZATION_FUNCS = {
    'iso': isoformat,
    'iso8601': isoformat,
    'rfc': rfcformat,
    'rfc822': rfcformat,
}

class DateTime(Field):
    """A formatted datetime string un UTC."""
    DEFAULT_FORMAT = 'iso'

    def __init__(self, format=None, **kwargs):
        super(DateTime, self).__init__(**kwargs)
        self.dateformat = format

    def format(self, value):
        if value:
            dateformat = self.dateformat or self.DEFAULT_FORMAT
            format_func = DATEFORMAT_SERIALIZATION_FUNCS.get(dateformat, None)
            try:
                if format_func:
                    return format_func(value)
                else:
                    return value.strftime(dateformat)
            except AttributeError as ae:
                raise MarshallingException(ae)
