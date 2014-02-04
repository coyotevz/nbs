# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

web = Blueprint('web', __name__,
                static_folder='static',
                template_folder='templates')

@web.route('/admin')
def admin():
    return render_template('admin.html')

@web.route('/pos')
def pos():
    return render_template('pos.html')
