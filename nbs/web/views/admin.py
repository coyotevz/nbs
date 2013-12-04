# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

admin = Blueprint('web.admin', __name__, url_prefix='/admin')

@admin.route('')
@admin.route('/products')
def show_admin():
    return render_template('admin/admin.html')
