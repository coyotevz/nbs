# -*- coding: utf-8 -*-

import requests
import json

class NobixConnection(object):

    def __init__(self, url, private_token=None):
        self._url = url
        self.headers = {
            'Content-Type': u'application/json',
            'Accept': u'application/json',
        }
        if private_token:
            self.headers['Private-Token'] = private_token

    def auth(self, username=None, password=None):
        ok = False
        if 'Private-Token' in self.headers:
            ok = self.token_auth()
        if not ok:
            self.credentials_auth(username, password)

    def token_auth(self):
        self.user = CurrentUser(self)
        try:
            self.user = CurrentUser(self)
            return True
        except:
            print "failed!"
            return False

    def credentials_auth(self, username, password):
        if not username or not password:
            raise Exception("Missing username/password")

        resp = self.raw_post('/auth/login', {'username': username,
                                             'password': password})
        if resp.status_code == 200:
            self.headers['Private-Token'] = resp.json()['private_token']
            self.token_auth()
        else:
            raise Exception(resp.json()['message'])

    def raw_post(self, path, data):
        url = '{}{}'.format(self._url, path)
        try:
            resp = requests.post(url, json.dumps(data), headers=self.headers)
        except:
            raise Exception("Can't connect to Nobix Application"
                            " Server ({})".format(self._url))
        return resp

    def raw_get(self, path):
        url = '{}{}'.format(self._url, path)
        try:
            resp = requests.get(url, headers=self.headers)
        except:
            raise Exception("Can't connect to Nobix Application"
                            " Server ({})".format(self._url))
        return resp

    def api_post(self, path, data):
        return self.raw_post('/api' + path, data)

    def api_get(self, path):
        return self.raw_get('/api' + path)

    def get(self, obj_class, id=None, **kwargs):
        url = obj_class._url
        if id is not None:
            url += '/{}'.format(id)
        resp = self.api_get(url)

        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception("Code Error returned ({}, {})".format(
                                   resp.status_code, ''))

class NobixRemoteObject(object):
    _url = None
    _id_attr = 'id'
    _constructor_types = None

    def __init__(self, conn, data=None, **kwargs):
        self.conn = conn

        if data is None or isinstance(data, int) or isinstance(data, str):
            data = self.conn.get(self.__class__, data, **kwargs)

        self._set_from_dict(data)

        if kwargs:
            for key, value in kwargs.iteritems():
                self.__dict__[key] = value

    def _set_from_dict(self, data):
        for key, value in data.iteritems():
            if isinstance(value, list):
                self.__dict__[key] = []
                for i in value:
                    self.__dict__[key].append(self._get_object(key, i))
            elif value:
                self.__dict__[key] = self._get_object(key, value)
            else: # None object
                self.__dict__[key] = None

    def _get_object(self, key, value):
        if self._constructor_types and key in self._constructor_types:
            return globals()[self._constructor_types[key]](self.conn, value)
        else:
            return value

    def __str__(self):
        return '{} => {}'.format(type(self), str(self.__dict__))


class CurrentUser(NobixRemoteObject):
    _url = '/user'
