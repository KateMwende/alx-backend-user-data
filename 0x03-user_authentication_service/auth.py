#!/usr/bin/env python3
import bcrypt
"""Making hash passwords with bcrypt"""


def _hash_password(password: str) -> bytes:
    """secure password further"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'),
                               salt)
    return hashed_pwd
