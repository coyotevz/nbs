# -*- coding: utf-8 -*-

from functools import wraps
from collections import namedtuple

from flask import current_app, request, url_for, render_template, redirect, g

from flask_principal import Principal, Permission, PermissionDenied, Need
from flask_principal import RoleNeed, UserNeed, AnonymousIdentity
from flask_principal import identity_changed, identity_loaded

from nbs.lib import auth
from nbs.models import User
from nbs.forms import LoginForm
from nbs.utils import jsonify, jsonify_status_code, jsonify_form, is_json

principals = Principal(use_sessions=False, skip_static=True)

# Super power permission
superuser_permission = Permission(RoleNeed('superuser'))

class Identity(object):
    """Represents the user's identity.

    :param id: The user id
    :param private_token: The private token used to confirm the user's
                          identity.

    This is a custom class that implements some behaviours required by Nobix
    Application Server.  An instance of this class fits the needs to use in
    Flask-Principal extension.
    """
    def __init__(self, id, private_token=None, data=None):
        self.id = id
        self.private_token = private_token
        self.data = data
        self.provides = set()

    def can(self, permission):
        return permission.allows(self) or superuser_permission.allows(self)

    def __repr__(self):
        return '<{0} id="{1}" private_token="{2}" provides={3}>'.format(
            self.__class__.__name__, self.id, self.private_token, self.provides
        )

LoginNeed = namedtuple('LoginNeed', '')

# Create a permission with a login need.
login_permission = Permission(LoginNeed())

def login_required(view):
    """Decorator to protect views to only loged in users"""
    @wraps(view)
    def decorated_view(*args, **kwargs):
        try:
            with login_permission.require():
                return view(*args, **kwargs)
        except PermissionDenied:
            return jsonify_status_code(401, message='401 Unauthorized')

    return decorated_view

def permission_required(permission):
    """Decorator to protect resource to certains permissions of users."""
    def decorator(view):
        @wraps(view)
        def decorated_view(*args, **kwargs):
            try:
                with permission.require():
                    return view(*args, **kwargs)
            except PermissionDenied:
                return jsonify_status_code(401, message='401 Unauthorized')
        return decorated_view
    return decorator

@principals.identity_loader
def identity_loader():
    """Called before request to find any provided identities."""
    pk = request.args.get('private_token', None)
    if not pk:
        pk = request.headers.get('Private-Token', None)
    if pk:
        data = auth.get_user_data(pk, True)
        if data:
            return Identity(data.user_id, private_token=pk, data=data)

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    """Signal received when an identity has been loaded for a request."""
    if not identity.id:
        return

    current_user = User.query.get(identity.id)
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(LoginNeed())
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
            for perm in role.permissions:
                identity.provides.add(Need(perm.action, perm.resource))

    if hasattr(current_user, 'permissions'):
        for perm in current_user.permissions:
            identity.provides.add(Need(perm.action, perm.resource))


## VIEWS ##

def login_view():
    if is_json(request):
        form = LoginForm(csrf_enabled=False)
    else:
        form = LoginForm()

    if form.validate_on_submit(): # authenticates the user too
        # TODO: set timeout for this user
        # TODO: set remote data for this user (hostname, etc.)
        pk = auth.set_user_data(form.user)
        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(form.user.id, pk))

        next_url = form.next.data

        if is_json(request):
            return jsonify({'login': 'OK', 'private_token': pk})
        else:
            # TODO: Set authentication data on return value (private_token)
            if not next_url or next_url == request.path:
                next_url = url_for('user.index', username=form.user.username)
            return redirect(next_url)

    if is_json(request):
        return jsonify_form(form)

    return render_template('login.html', form=form)


@login_required
def logout_view():
    user_data = auth.remove_user_data(g.identity.private_token)
    if user_data:
        msg = 'Loged out user {}'.format(user_data.user_id)
        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())
    else:
        msg = 'No user to logout'
    return jsonify({'message': msg})


@login_required
def test_view():
    from nbs.lib import rest

    identity=g.identity
    return jsonify(
        user=rest.to_dict(identity.user),
        data=identity.data._asdict(),
        needs=[getattr(p, '_asdict')() for p in identity.provides],
        other=current_app.user_data,
    )


## CONFIGURE ##

def configure_auth(app):
    auth.init_app(app)

    principals.init_app(app)

    app.add_url_rule('/auth/login', 'auth.login', login_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/auth/logout', 'auth.logout', logout_view)
    app.add_url_rule('/auth/test', 'auth.test', test_view)
