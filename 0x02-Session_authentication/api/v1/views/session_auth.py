#!/usr/bin/env python3
"""Flask view that handles all routes for the
Session authentication
"""
import os
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from typing import Tuple


@app_views.route('/auth_session/login',
                 methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    Handle user authentication.
    Retrieves email and password parameters from the request's form data.
    Verifies the provided email and password, and creates a session if valid.

    Returns:
        A tuple containing a JSON response and an HTTP status code.
    """
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    error_res = {"error": "no user found for this email"}
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(error_res), 404
    if len(users) <= 0:
        return jsonify(error_res), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """logout of a session using session id"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
