# -*- coding: utf-8 -*-

from pytest import raises
from tests import TestCase
from nbs.lib.rest import get_params, QueryParameters, OrderBy, Filter
from flask import request


class TestGetParams(TestCase):

    def get_params_for(self, qs):
        with self.app.test_client() as c:
            rv = c.get(qs)
            params = get_params()
        return params

    def test_single_filter(self):
        params = self.get_params_for('/?a=5')
        assert params.filters == [Filter('a', 'eq', '5')]

    def test_repeated_filter(self):
        params = self.get_params_for('/?b=3&b=4')
        assert params.filters == [Filter('b', 'eq', '3'),
                                  Filter('b', 'eq', '4')]

    def test_filter_with_operations(self):
        params = self.get_params_for('/?sku=20520&price:gt=3.20')
        assert params.filters == [Filter('sku', 'eq', '20520'),
                                  Filter('price', 'gt', '3.20')]

    def test_filter_with_repeated_operations(self):
        params = self.get_params_for('/?sku:endswith=101&sku:gt=200')
        assert params.filters == [Filter('sku', 'endswith', '101'),
                                  Filter('sku', 'gt', '200')]

    def test_sort_order(self):
        params = self.get_params_for('/?sort=description')
        assert params.sort == [OrderBy('description', 'asc')]
        params = self.get_params_for('/?sort=sku&sort:desc=price')
        assert params.sort == [OrderBy('sku', 'asc'), OrderBy('price', 'desc')]

    def test_page(self):
        params = self.get_params_for('/?page=5&page=4')
        assert params.page == 5
        params = self.get_params_for('/?page:gt=10&page=0')
        assert params.page == 10
        params = self.get_params_for('/?page:neq=1')
        assert params.page == 1

    def test_per_page(self):
        params = self.get_params_for('/?per_page=5&per_page=8')
        assert params.per_page == 5
        params = self.get_params_for('/?per_page:gt=10&per_page=1')
        assert params.per_page == 10
        params = self.get_params_for('/?per_page:neq=1')
        assert params.per_page == 1

    def test_single(self):
        params = self.get_params_for('/?single=1&single=6')
        assert params.single is True
        params = self.get_params_for('/?single=0&single=1')
        assert params.single is False
        params = self.get_params_for('/?single:not_equal_to=8')
        assert params.single is True

    def test_fields(self):
        params = self.get_params_for('/?fields=sku')
        assert params.fields == [u'sku']
        params = self.get_params_for('/?fields=sku&fields=description')
        assert params.fields == [u'sku', u'description']
        params = self.get_params_for('/?fields:gt=sku&sort=sku&fields:noop=test')
        assert params.fields == [u'sku', u'test']
