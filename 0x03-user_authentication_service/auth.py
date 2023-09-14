#!/usr/bin/env python3
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
"""Making hash passwords with bcrypt"""


def _hash_password(password: str) -> bytes:
    """secure password further"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'),
                               salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registering users, return a User object"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User {} already exists'.format(email))
