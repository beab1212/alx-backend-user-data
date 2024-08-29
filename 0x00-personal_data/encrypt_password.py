#!/usr/bin/env python3
"""
Encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
