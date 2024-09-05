#!/usr/bin/env python3
"""Session authentication with expiration
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


SESSION_DURATION = int(getenv('SESSION_DURATION', default=0))


class SessionExpAuth(SessionAuth):
    """Session aut with expiration
    """
    def __init__(self) -> None:
        """ Initialize a SessionAuth instance
        """
        super().__init__()
        self.session_duration = SESSION_DURATION

    def create_session(self, user_id: str = None) -> str:
        """doc
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        current_time = datetime.now()
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': current_time}
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """doc
        """
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        print("Debugging: ", session_data)
        if session_data is None:
            return None
        if self.session_duration <= 0:
            return session_data.get('user_id')
        if session_data.get('created_at') is None:
            return None
        if (session_data.created_at +
                timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None
        return super().user_id_for_session_id(session_id).get('user_id')
