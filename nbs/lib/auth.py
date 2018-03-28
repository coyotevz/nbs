# -*- coding: utf-8 -*-

import random, string
from collections import namedtuple
from datetime import datetime
from flask import current_app, g

UserData = namedtuple('UserData', ['user_id', 'login_time', 'last_access',
                                   'timeout', 'remote'])

def generate_private_token(size=20, chars=None):
    if not chars:
        chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for x in range(size))

def check_expired(remove=True):
    meth = dict.pop if remove else dict.get
    now = datetime.utcnow()
    retlist = []
    for key, data in list(current_app.user_data.items()):
        user_timeout = data.timeout
        if user_timeout > 0 and\
           now - login_time > datetime.timedelta(seconds=user_timeout):
            retlist.append(meth(current_app.user_data, None))
    return retlist

def check_unique(user_id, retrieve=False):
    for key, data in current_app.user_data.items():
        if data.user_id == user_id:
            return data if retrieve else False
    return True

def get_user_data(private_token, mark_access=True):
    check_expired()
    data = current_app.user_data.get(private_token, None)
    if data and mark_access:
        data = data._replace(last_access=datetime.utcnow())
        current_app.user_data[private_token] = data
    return data

def set_user_data(user, timeout=None, remote=None):

    if not check_unique(user.id):
        raise Exception("The user already has been loged in")

    check_expired()

    now = datetime.utcnow()
    if not timeout:
        timeout = 0
    user_data = UserData(user.id, now, now, timeout, remote)
    pk = generate_private_token()
    current_app.user_data[pk] = user_data
    return pk

def remove_user_data(token):
    check_expired()
    data = current_app.user_data.pop(token, None)
    return data

def remove_current_user_data():
    if hasattr(g, 'private_token'):
        pk = g.private_token # private token
        return remove_user_data(pk)
    return None

def init_app(app):
    app.user_data = {}
