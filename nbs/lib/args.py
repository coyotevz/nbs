# -*- coding: utf-8 -*-

import six
from flask import request


class _Missing(object):
    """Represents a value that is missing from the set of passed in request
    arguments."""

    def __bool__(self):
        return False

    __nonzero__ = __bool__ # py2 compatibility

    def __repr__(self):
        return '<nbs.lib.missing>'


#: Singleton object that represents a value that cannot be found on a request.
Missing = _Missing()


def get_value(data, name, multiple):
    """Get a value from a dictionary. Handles ``MultiDict`` types when
    ``multiple=True``. If the value is not found, return `missing`.
    """
    val = data.get(name, Missing)
    if multiple:
        if hasattr(data, 'getlist'):
            return data.getlist(name)
        else:
            return [val]
    return val


def noop(x):
    return x


class Argument(object):
    """A request argument."""

    def __init__(self, type=None, default=None, required=False, multiple=False,
                 allow_missing=False, target=None, source=None):
        self.type = type or noop
        if multiple and default is None:
            self.default = []
        else:
            self.default = default
        self.required = required
        self.multiple = multiple
        if required and allow_missing:
            raise ValueError('"required" and "allow_missing" cannot be True.')
        self.allow_missing = allow_missing
        self.target = target
        self.source = source


class Parser(object):

    DEFAULT_TARGETS = ('querystring', 'form', 'json')

    #: Maps target => method name
    TARGET_MAP = {
        'json': 'parse_json',
        'querystring': 'parse_querystring',
        'form': 'parse_form',
        'headers': 'parse_headers',
        'cookies': 'parse_cookies',
        'files': 'parse_files',
    }

    def __init__(self, targets=None, error_handler=None, error=None):
        self.targets = targets or self.DEFAULT_TARGETS
        self.error_callback = error_handler
        self.error = error

    def _validated_targets(self, targets):
        """Ensure that the given targets arguments is valid."""
        # The set difference between the givne targets and the available
        # targets will be the set of invalid targets
        valid_targets = set(self.TARGET_MAP.keys())
        given = set(targets)
        invalid_targets = given - valid_targets
        if len(invalid_targets):
            msg = "Invalid targets arguments: {0}".format(list(invalid_targets))
            raise ValueError(msg)
        return targets

    def _get_value(self, name, argobj, req, target):
        # Parsing function to call
        # May be a method name (str) or a function
        func = self.TARGET_MAP.get(target)
        if func:
            if inspect.isfunction(func):
                function = func
            else:
                function = getattr(self, func)
            value = function(req, argobj.source or name, argobj)
        else:
            value = None
        return value

    def parse_arg(self, name, argobj, req, targets=None):
        """Parse a single argument."""
        value = None
        if argobj.target:
            targets_to_check = self._validated_targets([argobj.target])
        else:
            targets_to_check = self._validated_targets(targets or self.targets)

        for target in targets_to_check:
            value = self._get_value(name, argobj, req=req, target=target)
            if argobj.multiple and not (isinstance(value, list) and len(value)):
                continue
            # Found the value: validate and return it
            if value is not Missing:
                return argobj.validated(value)
        if value is Missing:
            if argobj.default is not None:
                value = argobj.default
            if argobj.required:
                raise ValidationError('Required parameter {0!r} not found.'.format(name))
        return value

    def parse(self, argmap, req, targets=None, validate=None):
        """Main request parsing method."""
        try:
            parsed = {}
            for argname, argobj in six.iteritems(argmap):
                parsed_value = self.parse_arg(argname, argobj, req,
                                              targets=targets or self.targets)
                # Skip missing values
                can_skip = parsed_value is Missing or\
                           (argobj.multiple and not len(parsed_value))
                if argobj.allow_missing and can_skip:
                    continue
                else:
                    if parsed_value is Missing:
                        parsed_value = self.fallback(req, argname, argobj)
                    parsed[argname] = parsed_value
            if iscallable(validate):
                if not validate(parsed):
                    msg = u'Validator {0}({1}) is not True'.format(
                            validate.__name__, parsed
                    )
                    raise ValidationError(self.error or msg)
            return parsed
        except Exception as error:
            if self.error_callback:
                self.error_callback(error)
            else:
                self.handle_error(error)

    def parse_json(self, req, name, arg):
        """Pull a JSON value from a request object or return `Missing` if the
        value cannot be found."""
        return Missing

    def parse_querystring(self, req, name, arg):
        """Pull a value from query string of a request object or return
        `Missing` if the value cannot be found."""
        return Missing

    def parse_form(self, req, name, arg):
        """Pull a value from the form data of a request object or return
        `Missing` if the value cannot be found."""
        return Missing

    def parse_headers(self, req, name, arg):
        """Pull a value from the headers or return `Missing` if the value
        cannot be found."""
        return Missing
