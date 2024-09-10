#!/usr/bin/env python3
"""
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """return salted and hashed password byte
    """
    salt = bcrypt.gensalt(rounds=5)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
