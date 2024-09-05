#!/usr/bin/env python3
""" Session authentication
"""
from typing import TypeVar
from uuid import uuid4
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Authentication using session
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """ Initialize a SessionAuth instance
        """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Create session id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id from session_id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return session user from request cookie
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Remove session from the dictionary store
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
