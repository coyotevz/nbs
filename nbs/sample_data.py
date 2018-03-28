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
from nbs.models.document import DocumentItem, SaleInvoice

def install_fixtures():
    accesorios = ProductCategory(name='Accesorios')
    root = ProductCategory(name='Instalaciones Domiciliarias', children=[
        ProductCategory(name='Agua Fría y Caliente', children=[
            ProductCategory(name='GEN', children=[
                ProductCategory(name='GEN FUSION', children=[
                    accesorios,
                    ProductCategory(name='Tubos'),
                ]),
                ProductCategory(name='GEN ROSCA', children=[
                    ProductCategory(name='Accesorios'),
                    ProductCategory(name='Tubos'),
                ]),
            ]),
        ]),
    ])

    db.session.add(root)
    db.session.commit()

    gen = Supplier(name='GEN S.A.C.I. y F.', fancy_name='GEN', supplier_contacts=[
        SupplierContact(contact=Contact(first_name='Julio', last_name='Firchak'),
                        role='Representante Técnico'),
        SupplierContact(contact=Contact(first_name='Tereso', last_name='Acuña'),
                        role='Vendedor'),
        SupplierContact(contact=Contact(first_name='Sanguango', last_name='Quevedo'),
                        role='Representante Técnico'),
    ], fiscal_type=Supplier.FISCAL_RESPONSABLE_INSCRIPTO)
    der = Supplier(name='DER S.A.', supplier_contacts=[
        SupplierContact(contact=Contact(first_name='Ferrucio', last_name='Casimiro'),
                        role='Vendedor')
    ], fiscal_type=Supplier.FISCAL_RESPONSABLE_INSCRIPTO)

    db.session.add_all([gen, der])
    db.session.commit()

    w1 = Warehouse(name='Depósito Central')
    w2 = Warehouse(name='Depósito Godoy Cruz')
    b1 = Branch(name='Casa Central', fiscal_pos=1, warehouse=w1)
    b2 = Branch(name='Sucursal Godoy Cruz', fiscal_pos=2, warehouse=w2)
    o1 = Office(name='Oficina Administrativa')

    db.session.add_all([b1, b2, o1])
    db.session.commit()

    products = [
        {'s': '20120','d': 'CODO 90° HH Ø20 GEN FUSION','p': '2.21'},
        {'s': '20125','d': 'CODO 90° HH Ø25 GEN FUSION','p': '3.82'},
        {'s': '20132','d': 'CODO 90° HH Ø32 GEN FUSION','p': '5.32'},
        {'s': '20140','d': 'CODO 90° HH Ø40 GEN FUSION','p': '11.78'},
        {'s': '20150','d': 'CODO 90° HH Ø50 GEN FUSION','p': '22.14'},
        {'s': '20163','d': 'CODO 90° HH Ø63 GEN FUSION','p': '33.24'},
        {'s': '20175','d': 'CODO 90° HH Ø75 GEN FUSION','p': '87.51'},
        {'s': '20190','d': 'CODO 90° HH Ø90 GEN FUSION','p': '181.19'},
        {'s': '20320','d': 'TE HHH Ø20 GEN FUSION','p': '2.92'},
        {'s': '20325','d': 'TE HHH Ø25 GEN FUSION','p': '5.51'},
        {'s': '20332','d': 'TE HHH Ø32 GEN FUSION','p': '8.04'},
        {'s': '20340','d': 'TE HHH Ø40 GEN FUSION','p': '17.64'},
        {'s': '20350','d': 'TE HHH Ø50 GEN FUSION','p': '31.85'},
        {'s': '20363','d': 'TE HHH Ø63 GEN FUSION','p': '46.24'},
        {'s': '20375','d': 'TE HHH Ø75 GEN FUSION','p': '104.02'},
        {'s': '20390','d': 'TE HHH Ø90 GEN FUSION','p': '222.05'},
        {'s': '20520','d': 'CUPLA HH Ø20 GEN FUSION','p': '1.64'},
        {'s': '20525','d': 'CUPLA HH Ø25 GEN FUSION','p': '2.92'},
        {'s': '20532','d': 'CUPLA HH Ø32 GEN FUSION','p': '4.06'},
        {'s': '20540','d': 'CUPLA HH Ø40 GEN FUSION','p': '9.22'},
        {'s': '20550','d': 'CUPLA HH Ø50 GEN FUSION','p': '15.49'},
        {'s': '20563','d': 'CUPLA HH Ø63 GEN FUSION','p': '27.21'},
        {'s': '20575','d': 'CUPLA HH Ø75 GEN FUSION','p': '60.71'},
        {'s': '20590','d': 'CUPLA HH Ø90 GEN FUSION','p': '102.19'},
    ]

    bc = PriceComponent(name='Bonificación 36%', value=Decimal('36.00'))
    mc = PriceComponent(name='Markup 35%', value=Decimal('35.00'))
    unidad = ProductUnit.query.filter(ProductUnit.description=='Unidad').one()

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

    def p(sku):
        return Product.query.filter(Product.sku==sku).first()

    inv1 = SaleInvoice(issue_place=b1, number=12)
    inv1.items = [
        DocumentItem(product=p('20120'), quantity=5),
        DocumentItem(product=p('20125'), quantity=1),
        DocumentItem(product=p('20132'), quantity=7),
    ]

    db.session.add(inv1)

    inv2 = SaleInvoice(issue_place=b2, number=12, items=[
        DocumentItem(product=p('20350'), quantity=1),
        DocumentItem(product=p('20132'), quantity=3)
    ])
    inv2.fiscal_type = SaleInvoice.FISCAL_TYPE_A

    db.session.add(inv2)
    db.session.commit()

    inv2.issue()
    db.session.commit()
