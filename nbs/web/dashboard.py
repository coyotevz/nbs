# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

dashboard = Blueprint('web.dashboard', __name__)


@dashboard.route('/')
@dashboard.route('/dashboard')
def index():
    return render_template('dashboard/index.html')
