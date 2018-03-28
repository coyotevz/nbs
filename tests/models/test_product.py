# -*- coding: utf-8 -*-

from pytest import raises
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from tests import DBTestCase
from nbs.models.product import (
    ProductCategory, Product, ProductSupplierInfo, PriceComponent
)
from nbs.models.stock import StockTransaction
from nbs.models.supplier import Supplier
from nbs.models.places import Warehouse


class TestProductCategory(DBTestCase):

    def test_default_values(self):
        pc = ProductCategory(name='pc')
        self.db.session.add(pc)
        self.db.session.commit()
        assert pc.suggested_markup_components == []
        assert pc.suggested_commission == None


    def test_raises_with_null_name(self):
        pc = ProductCategory(suggested_commission=Decimal('1'))
        self.db.session.add(pc)
        with raises(IntegrityError):
            self.db.session.commit()

    def test_parent_commission(self):
        pc_parent = ProductCategory(name='pc_parent',
                                    suggested_commission=Decimal('2'))
        pc_child_1 = ProductCategory(name='pc_child_1',
                                     suggested_commission=Decimal('5'))
        pc_child_2 = ProductCategory(name='pc_child_2')

        pc_child_1.parent = pc_parent
        pc_child_2.parent = pc_parent

        self.db.session.add(pc_parent)
        self.db.session.commit()

        assert pc_parent.get_commission() == Decimal('2')
        assert pc_child_1.get_commission() == Decimal('5')
        assert pc_child_2.get_commission() == Decimal('2')

        pc_child_11 = ProductCategory(name='pc_child_11')
        pc_child_21 = ProductCategory(name='pc_child_21')

        pc_child_11.parent = pc_child_1
        pc_child_21.parent = pc_child_2

        self.db.session.commit()

        assert pc_child_11.get_commission() == Decimal('5')
        assert pc_child_21.get_commission() == Decimal('2')

    def test_parent_markup(self):
        pc_parent = ProductCategory(name='pc_parent')
        pc_child_1 = ProductCategory(name='pc_child_1')
        pc_child_2 = ProductCategory(name='pc_child_2')

        pc_p1 = PriceComponent(name='pc_p1', value=Decimal('30'))
        pc_p2 = PriceComponent(name='pc_p2', value=Decimal('5'))
        pc_c1 = PriceComponent(name='pc_c1', value=Decimal('65'))

        pc_parent.suggested_markup_components.extend([pc_p1, pc_p2])
        pc_child_1.suggested_markup_components.append(pc_c1)

        pc_child_1.parent = pc_parent
        pc_child_2.parent = pc_parent

        self.db.session.add(pc_parent)
        self.db.session.commit()

        assert list(pc_parent.get_markup()) == [Decimal('30'), Decimal('5')]
        assert list(pc_child_1.get_markup()) == [Decimal('65')]
        assert list(pc_child_2.get_markup()) == [Decimal('30'), Decimal('5')]

        pc_child_11 = ProductCategory(name='pc_child_11')
        pc_child_21 = ProductCategory(name='pc_child_21')

        pc_child_11.parent = pc_child_1
        pc_child_21.parent = pc_child_2

        self.db.session.commit()

        assert list(pc_child_11.get_markup()) == [Decimal('65')]
        assert list(pc_child_21.get_markup()) == [Decimal('30'), Decimal('5')]

    def test_get_path(self):
        pc_parent = ProductCategory(name='pc_parent')
        pc_child_1 = ProductCategory(name='pc_child_1', parent=pc_parent)
        pc_child_2 = ProductCategory(name='pc_child_2', parent=pc_parent)

        pc_child_11 = ProductCategory(name='pc_child_11', parent=pc_child_1)
        pc_child_12 = ProductCategory(name='pc_child_12', parent=pc_child_1)
        pc_child_21 = ProductCategory(name='pc_child_21', parent=pc_child_2)
        pc_child_22 = ProductCategory(name='pc_child_22', parent=pc_child_2)

        pc_child_211 = ProductCategory(name='pc_child_211',
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
        pc_parent = ProductCategory(name='pc_parent')
        pc_child_1 = ProductCategory(name='pc_child_1', parent=pc_parent)
        pc_child_2 = ProductCategory(name='pc_child_2', parent=pc_parent)

        pc_child_11 = ProductCategory(name='pc_child_11', parent=pc_child_1)
        pc_child_12 = ProductCategory(name='pc_child_12', parent=pc_child_1)
        pc_child_21 = ProductCategory(name='pc_child_21', parent=pc_child_2)
        pc_child_22 = ProductCategory(name='pc_child_22', parent=pc_child_2)

        pc_child_211 = ProductCategory(name='pc_child_211',
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


class TestProduct(DBTestCase):

    def test_default_status(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        self.db.session.add(p)
        self.db.session.commit()
        assert p.status == Product.STATUS_AVAILABLE

    def test_default_product_type(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        self.db.session.add(p)
        self.db.session.commit()
        assert p.product_type == Product.TYPE_PERMANENT

    def test_raise_duplicated_sku(self):
        p1 = Product(sku='123', description='p1', price=Decimal('1'))
        p2 = Product(sku='123', description='p2', price=Decimal('1'))

        self.db.session.add_all([p1, p2])
        with raises(IntegrityError):
            self.db.session.commit()

    def test_raises_for_commit_without_price(self):
        p = Product(sku='1', description='p1')
        self.db.session.add(p)
        with raises(IntegrityError):
            self.db.session.commit()

    def test_assert_price_before_flush(self):
        p = Product(sku='1', description='p1', automatic_price=True,
                    cost=Decimal('1.00'))
        p.markup_components.append(
            PriceComponent(name='pc1', value=Decimal('30'))
        )
        self.db.session.add(p)
        self.db.session.commit()
        assert p.price == Decimal('1.30')

    def test_automatic_price_flag_trigger(self):
        p = Product(sku='1', description='p1', price=Decimal('2.00'),
                    cost=Decimal('1.00'), automatic_price=False)
        p.markup_components.append(
            PriceComponent(name='pc1', value=Decimal('30'))
        )
        self.db.session.add(p)
        self.db.session.commit()
        p.automatic_price = True
        self.db.session.commit()
        assert p.price == Decimal('1.30')

    def test_cost_trigger(self):
        p = Product(sku='1', description='p1', automatic_price=True,
                    cost=Decimal('1.00'))
        pc1 = PriceComponent(name='pc1', value=Decimal('30.00'))
        pc2 = PriceComponent(name='pc2', value=Decimal('10.00'))
        p.markup_components.extend([pc1, pc2])
        self.db.session.add(p)
        self.db.session.commit()
        assert p.price == Decimal('1.43')
        p.cost = Decimal('2.00')
        self.db.session.commit()
        assert p.price == Decimal('2.86')

    def test_raise_on_invalid_stock_type(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w = Warehouse(name='w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        with raises(AssertionError):
            p.increase_stock(Decimal('10'), w, 'INVALID_TYPE', Decimal('1'))

        with raises(AssertionError):
            p.decrease_stock(Decimal('10'), w, 'INVALID_TYPE')

    def test_raise_negative_stock(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w = Warehouse(name='w')
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
        p = Product(sku='1', description='p1', price=Decimal('1'))
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
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w = Warehouse(name='w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        assert p.get_stock_items() == []

        p.register_initial_stock(Decimal('1'), w, Decimal('1'))
        self.db.session.commit()

        assert p.get_stock_items() != []

    def test_raises_register_initial_stock_with_transactions(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w1 = Warehouse(name='w1')
        self.db.session.add_all([p, w1])
        self.db.session.commit()

        p.register_initial_stock(Decimal('10'), w1, Decimal('1'))
        self.db.session.commit()

        p.decrease_stock(Decimal('2'), w1, StockTransaction.TYPE_SALE)

        with raises(ValueError):
            p.register_initial_stock(Decimal('1'), w1, Decimal('1'))

    def test_raise_on_decrease_with_not_existant_stock(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w = Warehouse(name='w')
        self.db.session.add_all([p, w])
        self.db.session.commit()

        with raises(ValueError):
            p.decrease_stock(Decimal('1'), w, StockTransaction.TYPE_SALE)

    def test_raise_on_decrease_more_than_available_stock(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w = Warehouse(name='w')
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
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w1 = Warehouse(name='w1')
        w2 = Warehouse(name='w2')
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

        p.decrease_stock(Decimal('1'), w1, StockTransaction.TYPE_SALE)
        self.db.session.commit()

        assert p.get_consolidated_stock() == Decimal('10')

    def test_get_stock_for_warehouse(self):
        p = Product(sku='1', description='p1', price=Decimal('1'))
        w1 = Warehouse(name='w1')
        w2 = Warehouse(name='w2')
        self.db.session.add_all([p, w1, w2])
        self.db.session.commit()

        p.register_initial_stock(Decimal('10'), w1, Decimal('1'))
        self.db.session.commit()

        assert p.get_stock_for_warehouse(w1).quantity == Decimal('10')
        assert p.get_stock_for_warehouse(w2).quantity == Decimal('0')


class TestProductSupplierInfo(DBTestCase):

    def test_defaults(self):
        p = Product(sku='1', description='p', price=Decimal('1'))
        s = Supplier(name='s1')

        psi = ProductSupplierInfo(supplier=s, product=p)

        self.db.session.add(psi)
        self.db.session.commit()

        assert psi.supplier_id == s.supplier_id
        assert psi.product_id == p.id
        assert psi.sku is None
        assert psi.automatic_cost == False
        assert psi.minimum_purchase == 1
        assert psi.package_size == 1
        assert psi.lead_time is None

    def test_automatic_cost(self):
        p = Product(sku='1', description='p', price=Decimal('1'))
        s = Supplier(name='s')
        psi = ProductSupplierInfo(supplier=s, product=p, automatic_cost=True,
                                  base_cost=Decimal('10'))
        bc1 = PriceComponent(name='bc1', value=Decimal('30'))
        bc2 = PriceComponent(name='bc2', value=Decimal('10'))
        psi.bonus_components.extend([bc1, bc2])

        self.db.session.add(psi)
        self.db.session.commit()

        assert psi.cost == Decimal('6.30')

    def test_base_cost_change(self):
        p = Product(sku='1', description='p', price=Decimal('1'))
        s = Supplier(name='s')
        psi = ProductSupplierInfo(supplier=s, product=p, automatic_cost=True,
                                  base_cost=Decimal('10'))
        bc1 = PriceComponent(name='bc1', value=Decimal('30'))
        bc2 = PriceComponent(name='bc2', value=Decimal('10'))
        psi.bonus_components.extend([bc1, bc2])

        self.db.session.add(psi)
        self.db.session.commit()

        assert psi.cost == Decimal('6.30')

        psi.base_cost = Decimal('20')
        assert psi.cost == Decimal('12.6')


    def test_automatic_cost_listener(self):
        p = Product(sku='1', description='p', price=Decimal('1'),
                    automatic_cost=True)
        s = Supplier(name='s')
        psi = ProductSupplierInfo(supplier=s, product=p, cost=Decimal('5'))
        self.db.session.add(psi)
        self.db.session.commit()

        assert p.cost == Decimal('5')

        psi.cost = Decimal('8')
        assert p.cost == Decimal('8')

    def test_automatic_assign_main_supplier(self):
        p = Product(sku='1', description='p', price=Decimal('1'),
                    automatic_cost=True)
        s1 = Supplier(name='s1')
        s2 = Supplier(name='s2')

        assert p.main_supplier_info == None
        psi1 = ProductSupplierInfo(supplier=s1, product=p, cost=Decimal('5'))
        assert p.main_supplier_info.supplier == s1
        psi2 = ProductSupplierInfo(supplier=s2, product=p, cost=Decimal('10'))
        assert p.main_supplier_info.supplier == s1
        self.db.session.add(p)
        self.db.session.commit()
        assert p.main_supplier_info.supplier == s1

        assert p.main_supplier_info == psi1

    def test_automatic_cost_listener_for_main_supplier(self):
        p = Product(sku='1', description='p', price=Decimal('1'),
                    automatic_cost=True)
        s1 = Supplier(name='s1')
        s2 = Supplier(name='s2')

        psi1 = ProductSupplierInfo(supplier=s1, product=p, cost=Decimal('5'))
        psi2 = ProductSupplierInfo(supplier=s2, product=p, cost=Decimal('10'))
        self.db.session.add(p)
        self.db.session.commit()

        assert p.cost == Decimal('5')
        psi2.cost = Decimal('8')
        assert p.cost == Decimal('5')
        psi1.cost = Decimal('6')
        assert p.cost == Decimal('6')


    def test_automatic_cost_flag_trigger(self):
        p = Product(sku='1', description='p', price=Decimal('1'))
        s = Supplier(name='s')

        psi = ProductSupplierInfo(supplier=s, product=p, cost=Decimal('5'),
                                  base_cost=Decimal('10'),
                                  automatic_cost=False)
        bc1 = PriceComponent(name='bc1', value=Decimal('30'))
        bc2 = PriceComponent(name='bc2', value=Decimal('10'))
        psi.bonus_components.extend([bc1, bc2])

        self.db.session.add(psi)
        self.db.session.commit()

        assert psi.cost == Decimal('5')

        psi.automatic_cost = True
        assert psi.cost == Decimal('6.3')


class TestPriceComponent(DBTestCase):

    def test_defaults(self):
        pc = PriceComponent(value=Decimal('1'))
        self.db.session.add(pc)
        self.db.session.commit()

        assert pc.name == None
        assert pc.value == Decimal('1')

    def test_raises_with_none_value(self):
        pc = PriceComponent(name='pc')
        self.db.session.add(pc)
        with raises(IntegrityError):
            self.db.session.commit()

    def test_trigger_product_price_change(self):
        p = Product(sku='1', description='p', cost=Decimal('10'),
                    automatic_price=True)
        pc1 = PriceComponent(name='pc1', value=Decimal('30'))
        pc2 = PriceComponent(name='pc2', value=Decimal('10'))

        p.markup_components.extend([pc1, pc2])

        self.db.session.add(p)
        self.db.session.commit()

        assert p.price == Decimal('14.3')

        pc1.value = Decimal('40')
        assert p.price == Decimal('15.4')

        pc2.value = Decimal('20')
        assert p.price == Decimal('16.8')

    def test_trigger_psi_cost_change(self):
        p = Product(sku='1', description='p', price=Decimal('1'))
        s1 = Supplier(name='s1')
        s2 = Supplier(name='s2')

        ps1 = ProductSupplierInfo(product=p, supplier=s1,
                                  base_cost=Decimal('20'),
                                  automatic_cost=True)
        ps2 = ProductSupplierInfo(product=p, supplier=s2,
                                  base_cost=Decimal('30'),
                                  automatic_cost=True)

        pc1 = PriceComponent(name='pc1', value=Decimal('10'))
        pc2 = PriceComponent(name='pc2', value=Decimal('20'))

        ps1.bonus_components.append(pc1)
        ps2.bonus_components.extend([pc1, pc2])

        self.db.session.add(p)
        self.db.session.commit()

        assert ps1.cost == Decimal('18')
        assert ps2.cost == Decimal('21.6')

        pc1.value = Decimal('5')

        assert ps1.cost == Decimal('19')
        assert ps2.cost == Decimal('22.8')
