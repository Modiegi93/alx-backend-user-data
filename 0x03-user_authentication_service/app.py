#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth
from sqlalchemy.exc import InvalidRequestError

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def welcome() -> str:
    """Return a payload form"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """implement the end-point to register a user"""
    try:
        email = request.form['email']
        password = request.form['password']

        user = AUTH.register_user(email, password)
        return jsonify(email=user.email, message='user created'), 200
    except ValueError as e:
        return jsonify(message=str(e)), 400
    except InvalidRequestError:
        return jsonify(message='email already registered'), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Create a session for user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify(email=email, message='logged in')
        response.set_cookie('session_id', session_id)
        return response, 200
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Clear the session of existing user when they logout"""
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Retrieve profile of user using session ID"""
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    """Reset password of user"""
    try:
        email = request.form['email']
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    response_data = {"email": email, "reset_token": reset_token}

    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
