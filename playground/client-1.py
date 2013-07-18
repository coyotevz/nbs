# -*- coding: utf-8 -*-

import requests
import json


class Nobix(object):
    """
    Represents a Nobix Application Server connection
    """

    def __init__(self, url, private_token=None, username=None, password=None):
        self._url = '{}/api'.format(url)
        self.private_token = private_token
        self.username = username
        self.password = password
        self.headers = {}
        
    def auth(self):
        """
        Performs an authentication using either the private token, or the
        username/password pair.

        The user attribute will hold a CurrentUser object on success.
        """
        ok = False
        if self.private_token:
            ok = self.token_auth()
        if not ok:
            self.credentials_auth()


    def token_auth(self):
        try:
            self.user = CurrentUser(self)
            return True
        except:
            return False

    def credentials_auth(self):
        if not self.username or not self.password:
            raise Exception("Missing username/password")

        resp = self.raw_post('/session', {'username': self.username,
                                          'password': self.password}) 
        if resp.status_code == 201:
            self.user = CurrentUser(self, resp.json())
        else:
            raise Exception(resp.json()['message'])

        self.private_token = self.user.private_token
        self.headers['Private-Token'] = self.user.private_token

    def raw_get(self, path, with_token=False):
        url = '{}{}'.format(self._url, path)
        if with_token:
            url += '?private_token={}'.format(self.private_token)

        try:
            return requests.get(url)
        except requests.ConnectionError, err:
            raise Exception("Can't connect to Nobix Application Server")


class NobixRemoteObject(object):
    _url = None
    _id_attr = 'id'

    def __init__(self, nbx, data=None, **kwargs):
        self.nobix = nbx

        if data is None or isinstance(data, int) or isinstance(data, str):
            data = self.nobix.get(self.__class__, data, **kwargs)

        self._set_from_dict(data)

        if kwargs:
            for k, v in kwargs.items():
                self.__dict__[k] = v

    def __str__(self):
        return '{} => {}'.format(type(self), str(self.__dict__))

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

    @classmethod
    def list(cls, nbx, **kwargs):
        if not cls._url:
            raise NotImplementedError

        return nbx.list(cls, **kwargs)

    def short_print(self, depth=0):
        id = self.__dict__[self._id_attr]
        print("{}{}: {}".format(" " * depth * 2, self._id_attr, id))

    def json(self):
        return json.dumps(self.__dict__)


class Supplier(NobixRemoteObject):
    _url = '/supplier'
