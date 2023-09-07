#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_credentials = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_credentials
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """show the user email and password"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.\
            split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})

        if not users or len(users) == 0:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user based on the
        provided request's authorization header.
        Args:
            request (Request): The Flask request object. Default is None.
        Returns:
            User or None: The User instance if authenticated,
            or None if not authenticated
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        bs64_txt = self.extract_base64_authorization_header(auth_header)
        if bs64_txt is None:
            return None

        decoded_txt = self.decode_base64_authorization_header(bs64_txt)
        if decoded_txt is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_txt)
        if user_email is None or user_pwd is None:
            return None

        user_inst = self.user_object_from_credentials(user_email, user_pwd)
        return user_inst
