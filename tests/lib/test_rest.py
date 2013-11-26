# -*- coding: utf-8 -*-

from pytest import raises
from tests import TestCase
from nbs.lib.qrest import get_params
from flask import request


class TestGetParams(TestCase):

    def get_params_for(self, qs):
        with self.app.test_client() as c:
            rv = c.get(qs)
            params = get_params()
        return params

    def test_single(self):
        params = self.get_params_for('/?a=5')
        assert params == dict(a=[('eq', '5')])

    def test_repeated_param(self):
        params = self.get_params_for('/?b=3&b=4')
        assert params == dict(b=[('eq', '3'), ('eq', '4')])

    def test_with_operations(self):
        params = self.get_params_for('/?sku=20520&price:gt=3.20')
        assert params == dict(sku=[('eq', '20520')], price=[('gt', '3.20')])

    def test_with_repeated_operations(self):
        params = self.get_params_for('/?sku:endswith=101&sku:gt=200')
        assert params == dict(sku=[('endswith', '101'), ('gt', '200')])

    def test_sort_order_op(self):
        params = self.get_params_for('/?sort=sku&sort:desc=price')
        assert params == dict(sort=[('asc', 'sku'), ('desc', 'price')])
