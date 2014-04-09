# -*- coding: utf-8 -*-

from pytest import raises
from sqlalchemy.exc import IntegrityError

from tests import DBTestCase
from nbs.models.document import Document, STATUS_DRAFT
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

        assert doc.status == STATUS_DRAFT
