# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, url_for, current_app
from nbs.models import db, User
from nbs.lib import rest
from nbs.utils import jsonify_status_code

from sqlalchemy.exc import IntegrityError

user_api = Blueprint('api.user', __name__, url_prefix='/api/users')

_pf = ['resource', 'action']
def _user_permissions(user, fields=None):
    return [rest.to_dict(perm, fields or _pf) for perm in user.permissions]

_rf = ['id', 'name']
def _user_roles(user, fields=None):
    return [rest.to_dict(role, fields or _rf) for role in user.roles]

_user_relations_map = {
    'permissions': _user_permissions,
    'roles': _user_roles,
}

_spec = {
    'map': _user_relations_map,
    'required': ['id'],
    'defaults': ['id', 'username', 'created', 'modified'],
    'authorized': [],
}

@user_api.route('', methods=['GET'])
def list():
    params = rest.get_params(_spec)
    query = rest.get_query(User, params)
    # Never send password fields
    if 'password' in params.fields:
        params.fields.remove('password')
    result = rest.get_result(query, params)
    return jsonify(result)

@user_api.route('/<int:id>', methods=['GET'])
def get(id):
    params = rest.get_params(_spec)
    obj = User.query.get_or_404(id)
    if 'password' in params.fields:
        params.fields.remove('password')
    filtered = rest.filter_fields(obj.query, params)
    return jsonify(rest.to_dict(obj, filtered))

@user_api.route('', methods=['POST'])
def add():
    data = rest.get_data()
    props = rest.get_to_update(User, data)
    try:
        user = User(**props)
        db.session.add(user)
        db.session.commit()
        result = rest.to_dict(user, _spec['defaults'])
        url = url_for('.get', id=result['id'])
        headers = dict(Location=url)
        return jsonify_status_code(201, headers=headers, **result)
    except IntegrityError as exception:
        current_app.logger.exception(exception.message)
        rest.rest_abort(400, message=exception.message)

@user_api.route('/<int:id>', methods=['PUT', 'PUSH'])
def update(id):
    return 'PUT {0}'.format(id)

@user_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify_status_code(204)

# TODO: Move this method to authentication api
#@user.route('/login')
#def login():
#    username = request.args.get('username', None)
#    if username is not None:
#        session['username'] = username
#        msg = "Logged in as '{0}' user.".format(escape(username))
#    else:
#        msg = "username is not privided in url."
#    return jsonify({'message': msg})
#
#@user.route('/logout')
#def logout():
#    username = session.pop('username', None)
#    if username:
#        msg = "{0} logged out".format(escape(username))
#    else:
#        msg = "no user to logout"
#    return jsonify({'message': msg})
#
#@user.route('/test')
#def test():
#    if 'username' in session:
#        msg = "Logged in as '{0}'".format(escape(session['username']))
#    else:
#        msg = "You are not logged in"
#    return jsonify({'message': msg})
