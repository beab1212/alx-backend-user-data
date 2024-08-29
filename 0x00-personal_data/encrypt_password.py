#!/usr/bin/env python3
"""
Encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypt and salt user password """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
