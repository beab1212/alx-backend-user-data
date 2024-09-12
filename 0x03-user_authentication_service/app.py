#!/usr/bin/env python3
"""Flask web server
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """home route handler
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """users post handler
    """
    email = request.form['email']
    password = request.form['password']

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError as error:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login handler
    """
    email = request.form['email']
    password = request.form['password']
    if email is None or password is None:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_token = AUTH.create_session(email)
    res = jsonify({"email": f"{email}", "message": "logged in"})
    res.set_cookie('session_id', session_token)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
