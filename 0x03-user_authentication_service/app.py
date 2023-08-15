#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request
from auth import Auth
from sqlalchemy.exc import InvalidRequestError

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def welcome():
    """Return a payload form"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
