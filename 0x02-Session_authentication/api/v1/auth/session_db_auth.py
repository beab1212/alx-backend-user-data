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
        if not user_id:
            return None
        session_id = str(uuid.uuid4())
        if not session_id:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id from session store
        """
        if not session_id:
            return None
        if 'UserSession' not in DATA:
            return None
        session = UserSession.search({'session_id': session_id})
        if not session:
            return None
        session = session[0]
        if self.session_duration <= 0:
            return session.user_id

        created_at = session.created_at
        duration = timedelta(seconds=self.session_duration)
        if (created_at + duration) < datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """Remove session from the store
        """
        if not request:
            return False
        session_id = self.session_cookies(request)
        if not session_id:
            return False
        if 'UserSession' not in DATA:
            return False
        session = UserSession.search({'session_id': session_id})
        if not session:
            return False
        session = session[0]
        session.remove()
        return True
