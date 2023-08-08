#!/usr/bin/env python3
"""Basic Authentication module"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Class Basic Authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract Base 64 Authorization Header"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        encoded = authorization_header.split(' ', 1)[1]

        return encoded
