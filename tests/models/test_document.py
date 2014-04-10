# -*- coding: utf-8 -*-

from pytest import raises
from sqlalchemy.exc import IntegrityError

from tests import DBTestCase
from nbs.models.document import Document, SaleInvoice
from nbs.models.places import Place, Warehouse, Branch


class TestDocument(DBTestCase):

    def test_raises_with_null_issue_place(self):
        doc = Document()
        self.db.session.add(doc)
        with raises(IntegrityError):
            self.db.session.commit()

    def test_default_status(self):
        p = Place(name=u'p')
        doc = Document(issue_place=p)
        self.db.session.add(doc)
        self.db.session.commit()

        assert doc.status == Document.STATUS_DRAFT
        assert doc.status_str == u'Borrador'

    def test_issue_method(self):
        p = Place(name=u'p')
        doc = Document(issue_place=p)
        self.db.session.add(doc)
        self.db.session.commit()

        doc.issue()
        self.db.session.commit()

        assert doc.status == Document.STATUS_ISSUED
        assert doc.issue_date is not None

    def test_can_modify(self):
        p = Place(name=u'p')
        doc = Document(issue_place=p)
        self.db.session.add(doc)
        self.db.session.commit()

        assert doc.can_modify() is True

        doc.issue()
        assert doc.can_modify() is False


class TestSaleInvoice(DBTestCase):

    def test_default_fiscal_type(self):
        b = Branch(name=u'b', fiscal_pos=1)
        invoice = SaleInvoice(issue_place=b)
        self.db.session.add(invoice)
        self.db.session.commit()

        assert invoice.fiscal_type == SaleInvoice.FISCAL_TYPE_B
        assert invoice.fiscal_type_label == u'B'

    def test_enum_fiscal_types(self):
        b = Branch(name=u'b', fiscal_pos=1)
        invoice = SaleInvoice(issue_place=b)
        self.db.session.add(invoice)
        self.db.session.commit()

        for _type in SaleInvoice._fiscal_type.keys():
            invoice.fiscal_type = _type
            self.db.session.commit()
            assert invoice.fiscal_type == _type

        invoice.fiscal_type = u'INVALID'
        with raises(IntegrityError):
            self.db.session.commit()

    def test_defaults(self):
        b = Branch(name=u'b', fiscal_pos=1)
        invoice = SaleInvoice(issue_place=b)
        self.db.session.add(invoice)
        self.db.session.commit()

        assert invoice.number is None
        assert invoice._type == u'sale_invoice'

    def test_unique_constraint(self):
        """
        Document.number is unique for a determined 'issue_place' and determined
        'fiscal_type'.
        """
        b1 = Branch(name=u'b1', fiscal_pos=1)
        b2 = Branch(name=u'b2', fiscal_pos=2)

        si1 = SaleInvoice(fiscal_type=SaleInvoice.FISCAL_TYPE_A,
                          number=10, issue_place=b1)
        self.db.session.add(si1)
        self.db.session.commit()

        si2 = SaleInvoice(fiscal_type=SaleInvoice.FISCAL_TYPE_A,
                          number=10, issue_place=b2)
        self.db.session.add(si2)
        self.db.session.commit()

        si3 = SaleInvoice(fiscal_type=SaleInvoice.FISCAL_TYPE_B,
                          number=10, issue_place=b1)
        self.db.session.add(si3)
        self.db.session.commit()

        assert si1.number == si2.number
        assert si2.number == si3.number

        bad_si = SaleInvoice(fiscal_type=SaleInvoice.FISCAL_TYPE_A,
                             number=10, issue_place=b1)
        self.db.session.add(bad_si)
        with raises(IntegrityError):
            self.db.session.commit()
