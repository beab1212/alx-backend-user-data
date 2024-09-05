#!/usr/bin/env python3
"""Auth endpoints
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


SESSION_NAME = getenv('SESSION_NAME', None)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login handler
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session = auth.create_session(user.id)
            res = jsonify(user.to_json())
            res.set_cookie(SESSION_NAME, session)
            return res
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Logout handler
    """
    from api.v1.app import auth
    is_distorted = auth.destroy_session(request)
    if is_distorted is False:
        abort(404)
    return jsonify({}), 200
