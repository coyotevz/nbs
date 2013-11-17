# -*- coding: utf-8 -*-

from pytest import raises
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from tests import TestCase
from nbs.models.product import ProductCategory, Product, PriceComponent
from nbs.models.stock import StockTransaction
from nbs.models.places import Warehouse


class TestProductCategory(TestCase):

    def test_default_values(self):
        pc = ProductCategory(description=u'pc')
        self.db.session.add(pc)
        self.db.session.commit()
        assert pc.suggested_markup == None
        assert pc.suggested_commission == None


    def test_raises_with_null_description(self):
        pc = ProductCategory(suggested_markup=Decimal('30'),
                             suggested_commission=Decimal('1'))
        self.db.session.add(pc)
        with raises(IntegrityError):
            self.db.session.commit()

    def test_parent_commission(self):
        pc_parent = ProductCategory(description=u'pc_parent',
                                    suggested_commission=Decimal('2'))
        pc_child_1 = ProductCategory(description=u'pc_child_1',
                                     suggested_commission=Decimal('5'))
        pc_child_2 = ProductCategory(description=u'pc_child_2')

        pc_child_1.parent = pc_parent
        pc_child_2.parent = pc_parent

        self.db.session.add(pc_parent)
        self.db.session.commit()

        assert pc_parent.get_commission() == Decimal('2')
        assert pc_child_1.get_commission() == Decimal('5')
        assert pc_child_2.get_commission() == Decimal('2')

        pc_child_11 = ProductCategory(description=u'pc_child_11')
        pc_child_21 = ProductCategory(description=u'pc_child_21')

        pc_child_11.parent = pc_child_1
        pc_child_21.parent = pc_child_2

        self.db.session.commit()

        assert pc_child_11.get_commission() == Decimal('5')
        assert pc_child_21.get_commission() == Decimal('2')

    def test_parent_markup(self):
        pc_parent = ProductCategory(description=u'pc_parent',
                                    suggested_markup=Decimal('30'))
        pc_child_1 = ProductCategory(description=u'pc_child_1',
                                     suggested_markup=Decimal('65'))
        pc_child_2 = ProductCategory(description=u'pc_child_2')

        pc_child_1.parent = pc_parent
        pc_child_2.parent = pc_parent

        self.db.session.add(pc_parent)
        self.db.session.commit()

        assert pc_parent.get_markup() == Decimal('30')
        assert pc_child_1.get_markup() == Decimal('65')
        assert pc_child_2.get_markup() == Decimal('30')

        pc_child_11 = ProductCategory(description=u'pc_child_11')
        pc_child_21 = ProductCategory(description=u'pc_child_21')

        pc_child_11.parent = pc_child_1
        pc_child_21.parent = pc_child_2

        self.db.session.commit()

        assert pc_child_11.get_markup() == Decimal('65')
        assert pc_child_21.get_markup() == Decimal('30')

    def test_get_path(self):
        pc_parent = ProductCategory(description=u'pc_parent')
        pc_child_1 = ProductCategory(description=u'pc_child_1',
                                     parent=pc_parent)
        pc_child_2 = ProductCategory(description=u'pc_child_2',
                                     parent=pc_parent)

        pc_child_11 = ProductCategory(description=u'pc_child_11',
                                       parent=pc_child_1)
        pc_child_12 = ProductCategory(description=u'pc_child_12',
                                       parent=pc_child_1)
        pc_child_21 = ProductCategory(description=u'pc_child_21',
                                       parent=pc_child_2)
        pc_child_22 = ProductCategory(description=u'pc_child_22',
                                       parent=pc_child_2)

        pc_child_211 = ProductCategory(description=u'pc_child_211',
                                          parent=pc_child_21)

        self.db.session.add(pc_parent)
        self.db.session.commit()

        assert list(pc_parent.get_path()) == [pc_parent]
        assert list(pc_child_1.get_path()) == [pc_parent, pc_child_1]
        assert list(pc_child_22.get_path()) == [pc_parent, pc_child_2,
                                                pc_child_22]
        assert list(pc_child_211.get_path()) == [pc_parent, pc_child_2,
                                                 pc_child_21, pc_child_211]

    def test_get_children_recursively(self):
        pc_parent = ProductCategory(description=u'pc_parent')
        pc_child_1 = ProductCategory(description=u'pc_child_1',
                                     parent=pc_parent)
        pc_child_2 = ProductCategory(description=u'pc_child_2',
                                     parent=pc_parent)

        pc_child_11 = ProductCategory(description=u'pc_child_11',
                                       parent=pc_child_1)
        pc_child_12 = ProductCategory(description=u'pc_child_12',
                                       parent=pc_child_1)
        pc_child_21 = ProductCategory(description=u'pc_child_21',
                                       parent=pc_child_2)
        pc_child_22 = ProductCategory(description=u'pc_child_22',
                                       parent=pc_child_2)

        pc_child_211 = ProductCategory(description=u'pc_child_211',
                                          parent=pc_child_21)

        self.db.session.add(pc_parent)
        self.db.session.commit()

        assert list(pc_child_211.get_children_recursively()) == []
        assert list(pc_child_21.get_children_recursively()) == [pc_child_211]
        assert sorted(list(pc_child_1.get_children_recursively())) == \
                sorted([pc_child_12, pc_child_11])
        assert sorted(list(pc_child_2.get_children_recursively())) == \
                sorted([pc_child_211, pc_child_21, pc_child_22])
        assert sorted(list(pc_parent.get_children_recursively())) == \
                sorted([pc_child_1, pc_child_2, pc_child_11, pc_child_12,
                        pc_child_21, pc_child_22, pc_child_211])


class TestProduct(TestCase):

    def test_default_status(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        self.db.session.add(p)
        self.db.session.commit()
        assert p.status == Product.STATUS_AVAILABLE

    def test_default_product_type(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        self.db.session.add(p)
        self.db.session.commit()
        assert p.product_type == Product.TYPE_PERMANENT

    def test_raise_duplicated_sku(self):
        p1 = Product(sku=u'123', description=u'p1', price=Decimal('1'))
        p2 = Product(sku=u'123', description=u'p2', price=Decimal('1'))

        self.db.session.add_all([p1, p2])
        with raises(IntegrityError):
            self.db.session.commit()

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

    def test_raise_on_invalid_stock_type(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        w = Warehouse(name=u'w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        with raises(AssertionError):
            p.increase_stock(Decimal('10'), w, 'INVALID_TYPE', Decimal('1'))

        with raises(AssertionError):
            p.decrease_stock(Decimal('10'), w, 'INVALID_TYPE')

    def test_raise_negative_stock(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        w = Warehouse(name=u'w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        with raises(ValueError):
            p.increase_stock(Decimal('-1'), w,
                             StockTransaction.TYPE_RETURNED_SALE)

        with raises(ValueError):
            p.decrease_stock(Decimal('-1'), w, StockTransaction.TYPE_SALE)

        with raises(ValueError):
            p.register_initial_stock(Decimal('-4'), w, None)

    def test_raise_on_null_warehouse(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        self.db.session.add(p)
        self.db.session.commit()

        with raises(ValueError):
            p.increase_stock(Decimal('1'), None,
                             StockTransaction.TYPE_RETURNED_SALE)

        with raises(ValueError):
            p.decrease_stock(Decimal('1'), None, StockTransaction.TYPE_SALE)

        with raises(ValueError):
            p.register_initial_stock(Decimal('0'), None, None)

    def test_stock_creation(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        w = Warehouse(name=u'w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        assert p.get_stock_items() == []

        p.register_initial_stock(Decimal('1'), w, Decimal('1'))
        self.db.session.commit()

        assert p.get_stock_items() != []

    def test_raise_on_decrease_with_not_existant_stock(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        w = Warehouse(name=u'w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        with raises(ValueError):
            p.decrease_stock(Decimal('1'), w, StockTransaction.TYPE_SALE)

    def test_raise_on_decrease_more_than_available_stock(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        w = Warehouse(name=u'w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        p.register_initial_stock(Decimal('4'), w, Decimal('1'))
        self.db.session.commit()

        with raises(ValueError):
            p.decrease_stock(Decimal('5'), w, StockTransaction.TYPE_SALE)

        p.decrease_stock(Decimal('4'), w, StockTransaction.TYPE_SALE)
        self.db.session.commit()
        assert p.get_stock_items()[0].quantity == Decimal('0')

    def test_get_consolidated_stock(self):
        p = Product(sku=u'1', description=u'p1', price=Decimal('1'))
        w1 = Warehouse(name=u'w1')
        w2 = Warehouse(name=u'w2')
        self.db.session.add_all([p, w1, w2])
        self.db.session.commit()

        p.register_initial_stock(Decimal('10'), w1, Decimal('1'))
        p.register_initial_stock(Decimal('5'), w2, Decimal('1'))
        self.db.session.commit()

        assert p.get_consolidated_stock() == Decimal('15')

        p.decrease_stock(Decimal('2'), w1, StockTransaction.TYPE_SALE)
        p.decrease_stock(Decimal('2'), w2, StockTransaction.TYPE_SALE)
        self.db.session.commit()

        assert p.get_consolidated_stock() == Decimal('11')


class TestProductSupplierInfo(TestCase):
    pass


class TestPriceComponent(TestCase):
    pass
