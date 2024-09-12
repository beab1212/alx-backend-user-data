#!/usr/bin/env python3
"""Authentication provider
"""
import bcrypt
from uuid import uuid4
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """return salted and hashed password byte
    """
    salt = bcrypt.gensalt(rounds=5)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """generate uuid
    """
    uuid_str = str(uuid4())
    return uuid_str


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user into the database
        """
        # Note: NoResultFound raised if record doesn't exist only
        try:
            is_email_exist = self._db.find_user_by(email=email)
            raise ValueError(f"User {is_email_exist.email} already exists")
        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """validate credentials
        """
        try:
            is_user_exist = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),
                              is_user_exist.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create and attach session token to a user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_token = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_token)
            return session_token
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """return user by it's session id or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """deleting session_id by user id
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generate reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = str(uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """doc
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 password=_generate_uuid(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
