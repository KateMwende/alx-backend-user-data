#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """simple json string"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """implement the end-point to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["GET"], stict_slashes=False)
def login() -> str:
    """implement a login function"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)

    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
