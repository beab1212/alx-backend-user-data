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

        if session_id is None:
            return None

        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id from session store
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})

        if not user_sessions:
            return None

        user_session = user_sessions[0]

        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Remove session from the store
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
