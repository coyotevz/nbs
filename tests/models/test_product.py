# -*- coding: utf-8 -*-

from tests import TestCase
from nbs.models import Product


class TestSomething(TestCase):

    def test_get(self):
        response = self.client.get('/api/product')
        assert 200 == response.status_code
        response = self.client.get('/api/product/')
        assert 404 == response.status_code
        response = self.client.get('/api/products')
        assert 404 == response.status_code
