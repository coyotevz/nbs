# -*- coding: utf-8 -*-

"""Load initial data for test"""

from decimal import Decimal
from nbs.models import db
from nbs.models.contact import Contact
from nbs.models.product import ProductCategory, Product, create_primitive_units
from nbs.models.supplier import Supplier, SupplierContact

def install_fixtures():
    root = ProductCategory(name=u'Instalaciones Domiciliarias', children=[
        ProductCategory(name=u'Agua Fría y Caliente', children=[
            ProductCategory(name=u'GEN', children=[
                ProductCategory(name=u'GEN FUSION', children=[
                    ProductCategory(name=u'Accesorios'),
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
