#!/usr/bin/env python3
"""Module for expiration of Session Authentication"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Expiration Class"""

    def __init__(self):
        """Initialization"""
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            session_duration = int(SESSION_DURATION)
        except Exception:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create session with expiration"""

        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user_id from session_id"""
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None
