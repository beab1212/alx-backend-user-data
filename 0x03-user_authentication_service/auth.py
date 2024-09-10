#!/usr/bin/env python3
"""Authentication provider
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """return salted and hashed password byte
    """
    salt = bcrypt.gensalt(rounds=5)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user into the database
        """
        is_email_exist = self._db.find_user_by(email=email)
        if is_email_exist is not None:
            raise ValueError(f"User {is_email_exist.email} already exists")

        new_user = self._db.add_user(email, _hash_password(password))
        return new_user
