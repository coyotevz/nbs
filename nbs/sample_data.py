# -*- coding: utf-8 -*-

"""Load initial data for test"""

from decimal import Decimal
from random import randint
from nbs.models import db
from nbs.models.contact import Contact
from nbs.models.product import ProductCategory, Product, PriceComponent
from nbs.models.product import ProductSupplierInfo, ProductUnit
from nbs.models.supplier import Supplier, SupplierContact
from nbs.models.places import Warehouse, Branch, Office

def install_fixtures():
    accesorios = ProductCategory(name=u'Accesorios')
    root = ProductCategory(name=u'Instalaciones Domiciliarias', children=[
        ProductCategory(name=u'Agua Fría y Caliente', children=[
            ProductCategory(name=u'GEN', children=[
                ProductCategory(name=u'GEN FUSION', children=[
                    accesorios,
                    ProductCategory(name=u'Tubos'),
                ]),
                ProductCategory(name=u'GEN ROSCA', children=[
                    ProductCategory(name=u'Accesorios'),
                    ProductCategory(name=u'Tubos'),
                ]),
            ]),
        ]),
    ])

    db.session.add(root)
    db.session.commit()

    gen = Supplier(name=u'GEN S.A.C.I. y F.', fancy_name=u'GEN', supplier_contacts=[
        SupplierContact(contact=Contact(first_name=u'Julio', last_name=u'Firchak'),
                        role=u'Representante Técnico'),
        SupplierContact(contact=Contact(first_name=u'Tereso', last_name=u'Acuña'),
                        role=u'Vendedor'),
        SupplierContact(contact=Contact(first_name=u'Sanguango', last_name=u'Quevedo'),
                        role=u'Representante Técnico'),
    ], fiscal_type=Supplier.FISCAL_RESPONSABLE_INSCRIPTO)
    der = Supplier(name=u'DER S.A.', supplier_contacts=[
        SupplierContact(contact=Contact(first_name=u'Ferrucio', last_name=u'Casimiro'),
                        role=u'Vendedor')
    ], fiscal_type=Supplier.FISCAL_RESPONSABLE_INSCRIPTO)

    db.session.add_all([gen, der])
    db.session.commit()

    w1 = Warehouse(name=u'Depósito Central')
    w2 = Warehouse(name=u'Depósito Godoy Cruz')
    b1 = Branch(name=u'Casa Central', warehouse=w1)
    b2 = Branch(name=u'Sucursal Godoy Cruz', warehouse=w2)
    o1 = Office(name=u'Oficina Administrativa')

    db.session.add_all([b1, b2, o1])
    db.session.commit()

    products = [
        {'s': u'20120','d': u'CODO 90° HH Ø20 GEN FUSION','p': '2.21'},
        {'s': u'20125','d': u'CODO 90° HH Ø25 GEN FUSION','p': '3.82'},
        {'s': u'20132','d': u'CODO 90° HH Ø32 GEN FUSION','p': '5.32'},
        {'s': u'20140','d': u'CODO 90° HH Ø40 GEN FUSION','p': '11.78'},
        {'s': u'20150','d': u'CODO 90° HH Ø50 GEN FUSION','p': '22.14'},
        {'s': u'20163','d': u'CODO 90° HH Ø63 GEN FUSION','p': '33.24'},
        {'s': u'20175','d': u'CODO 90° HH Ø75 GEN FUSION','p': '87.51'},
        {'s': u'20190','d': u'CODO 90° HH Ø90 GEN FUSION','p': '181.19'},
        {'s': u'20320','d': u'TE HHH Ø20 GEN FUSION','p': '2.92'},
        {'s': u'20325','d': u'TE HHH Ø25 GEN FUSION','p': '5.51'},
        {'s': u'20332','d': u'TE HHH Ø32 GEN FUSION','p': '8.04'},
        {'s': u'20340','d': u'TE HHH Ø40 GEN FUSION','p': '17.64'},
        {'s': u'20350','d': u'TE HHH Ø50 GEN FUSION','p': '31.85'},
        {'s': u'20363','d': u'TE HHH Ø63 GEN FUSION','p': '46.24'},
        {'s': u'20375','d': u'TE HHH Ø75 GEN FUSION','p': '104.02'},
        {'s': u'20390','d': u'TE HHH Ø90 GEN FUSION','p': '222.05'},
        {'s': u'20520','d': u'CUPLA HH Ø20 GEN FUSION','p': '1.64'},
        {'s': u'20525','d': u'CUPLA HH Ø25 GEN FUSION','p': '2.92'},
        {'s': u'20532','d': u'CUPLA HH Ø32 GEN FUSION','p': '4.06'},
        {'s': u'20540','d': u'CUPLA HH Ø40 GEN FUSION','p': '9.22'},
        {'s': u'20550','d': u'CUPLA HH Ø50 GEN FUSION','p': '15.49'},
        {'s': u'20563','d': u'CUPLA HH Ø63 GEN FUSION','p': '27.21'},
        {'s': u'20575','d': u'CUPLA HH Ø75 GEN FUSION','p': '60.71'},
        {'s': u'20590','d': u'CUPLA HH Ø90 GEN FUSION','p': '102.19'},
    ]

    bc = PriceComponent(name=u'Bonificación 36%', value=Decimal('36.00'))
    mc = PriceComponent(name=u'Markup 35%', value=Decimal('35.00'))
    unidad = ProductUnit.query.filter(ProductUnit.description==u'Unidad').one()

    for p in products:

        pro = Product(sku=p['s'], description=p['d'], automatic_price=True,
                      automatic_cost=True, markup_components=[mc],
                      category=accesorios, unit=unidad)

        psi = ProductSupplierInfo(supplier=gen, product=pro,
                description=p['d'][:-11], base_cost=Decimal(p['p']),
                automatic_cost=True, bonus_components=[bc])

        for w in (w1, w2):
            pro.register_initial_stock(randint(randint(0,10), randint(10, 60)), w, pro.cost)

        db.session.add(pro)

    db.session.commit()
