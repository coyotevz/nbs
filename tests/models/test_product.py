# -*- coding: utf-8 -*-

from pytest import raises
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from tests import TestCase
from nbs.models import Product, PriceComponent


class TestProduct(TestCase):

    def test_raises_for_commit_without_price(self):
        p = Product(sku=u'1', description=u'p1')
        self.db.session.add(p)
        with raises(IntegrityError):
            self.db.session.commit()

    def test_assert_price_before_flush(self):
        p = Product(sku=u'1', description=u'p1', automatic_price=True,
                    cost=Decimal('1.00'))
        p.markup_components.append(
            PriceComponent(name=u'pc1', value=Decimal('30'))
        )
        self.db.session.add(p)
        self.db.session.commit()
        assert p.price == Decimal('1.30')

    def test_automatic_price_flag_trigger(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('2.00'),
                    cost=Decimal('1.00'), automatic_price=False)
        p.markup_components.append(
            PriceComponent(name=u'pc1', value=Decimal('30'))
        )
        self.db.session.add(p)
        self.db.session.commit()
        p.automatic_price = True
        self.db.session.commit()
        assert p.price == Decimal('1.30')

    def test_cost_trigger(self):
        p = Product(sku=u'1', description=u'p1', automatic_price=True,
                    cost=Decimal('1.00'))
        pc1 = PriceComponent(name=u'pc1', value=Decimal('30.00'))
        pc2 = PriceComponent(name=u'pc2', value=Decimal('10.00'))
        p.markup_components.extend([pc1, pc2])
        self.db.session.add(p)
        self.db.session.commit()
        assert p.price == Decimal('1.43')
        p.cost = Decimal('2.00')
        self.db.session.commit()
        assert p.price == Decimal('2.86')


class TestProductSupplierInfo(TestCase):
    pass


class TestPriceComponent(TestCase):
    pass
