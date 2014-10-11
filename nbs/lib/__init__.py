# -*- coding: utf-8 -*-

from collections import OrderedDict

def marshal(data, fields):
    """
    Takes a raw data (in the form of a dict, list, object) and a dict of fields
    to output and filters the data based on thouse fields.

    :param data: the actual object(s) form which the fields are taken from
    :param fields: a dict of whose keys will make up the final serialized
                   response output
    """
    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls

    if isinstance(data, (list, tuple)):
        return [marshal(d, fields) for d in data]

    items = ((k, marshal(data, v) if isinstance(v, dict)
              else make(v).output(k, data))
              for k, v in fields.iteritems())
    return OrderedDict(items)
