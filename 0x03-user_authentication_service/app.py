#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, make_response, abort
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
def login():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
