# -*- coding: utf-8 -*-

from flask import request
from wtforms.compat import iteritems
from wtforms.fields import StringField
from wtforms.validators import DataRequired
from nbs.models import db

def string_field_process_formdata(self, valuelist):
    if valuelist:
        self.data = valuelist[0]
    elif not self.data:
        self.data = ''

# patch process_formdata for string field.
StringField.process_formdata = string_field_process_formdata

from wtforms_alchemy import model_form_factory
from flask.ext.wtf import Form as _Form

class Form(_Form):

    def is_submitted(self):
        return request and request.method in ("PUT", "PATCH", "POST")

    @property
    def patch_data(self):
        data = {}

        for name, f in iteritems(self._fields):
            if f.raw_data and (f.data != f.object_data):
                data[name] = f.data

        return data

    def patch_obj(self, obj):
        """
        Patch the attributes of the passed `obj` with data from the form's
        changed fields.

        :note: This method like :meth:`~Form.populate_obj` is a destructive
               operation; Any attribute with the same name as a filld will be
               overridden. Use with caution.
        """
        for name in self.patch_data:
            field = self._fields.get(name)
            field.populate_obj(obj, name)


options = {
    'not_null_validator': DataRequired(),
    'not_null_validator_type_map': {},
}

BaseModelForm = model_form_factory(Form, **options)

class ModelForm(BaseModelForm):

    @classmethod
    def get_session(self):
        return db.session
