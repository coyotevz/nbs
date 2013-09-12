# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from nbs.models import db, Product

pos = Blueprint('web.pos', __name__, url_prefix='/pos')

@pos.route('/')
def index():
    return render_template('pos/pos.html')
