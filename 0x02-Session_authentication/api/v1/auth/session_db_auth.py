#!/usr/bin/env python3
"""Session management with persistance
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session management with persistance
    """
    def create_session(self, user_id: str = None) -> str:
        """Create session id and store it
        """
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id from session store
        """
        if session_id:
            user_session = UserSession.search({'session_id': session_id})
            if user_session and self.session_duration > 0:
                return user_session[0].user_id

    def destroy_session(self, request=None):
        """Remove session from the store
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_session = UserSession.search({'session_id': session_id})
                if user_session:
                    user_session[0].remove()
                    return True
        return False
