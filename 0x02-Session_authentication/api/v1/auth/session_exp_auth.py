#!/usr/bin/env python3
"""Session authentication with expiration
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session aut with expiration
    """
    def __init__(self) -> None:
        """ Initialize a SessionAuth instance
        """
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', default=0))

    def create_session(self, user_id: str = None) -> str:
        """doc
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """doc
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id[session_id]
        user_id = session_data.get('user_id')

        if self.session_duration <= 0:
            return user_id

        created_at = session_data.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
