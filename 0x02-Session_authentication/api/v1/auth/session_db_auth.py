#!/usr/bin/env python3
"""Session management with persistance
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session management with persistance
    """
    def __init__(self) -> None:
        """Initialize a SessionAuth instance
        """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Create session id and store it
        """
        session_id = super().create_session(user_id)
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id from session store
        """
        user_id = UserSession.search({'session_id': session_id})
        if len(session_id) == 0:
            return None
        user_id = user_id[0].get('user_id')
        return user_id

    def destroy_session(self, request=None):
        """Remove session from the store
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        session_object = UserSession.search({'session_id': session_id})
        if len(session_id) == 0:
            return False
        session_object[0].remove()

        return super().destroy_session(request)
