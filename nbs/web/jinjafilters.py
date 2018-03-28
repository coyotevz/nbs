# -*- coding: utf-8 -*-

from decimal import Decimal
import random

def datefmt_filter(date, format="%d %b, %Y"):
    if date:
        return date.strftime(format)
    return ''

def moneyfmt_filter(value, places=2, curr='', sep='.', dp=',',
                     pos='', neg='-', trailneg=''):
    value = Decimal(value)
    q = Decimal(10) ** -places
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))

def configure_jinja(app):

    # extensions
    app.jinja_options['extensions'].extend([
        'jinja2.ext.i18n',
        'jinja2.ext.do',
        'jinja2.ext.with_',
        'jinja2.ext.loopcontrols',
    ])

    # filters
    app.jinja_env.filters['datefmt'] = datefmt_filter
    app.jinja_env.filters['moneyfmt'] = moneyfmt_filter
