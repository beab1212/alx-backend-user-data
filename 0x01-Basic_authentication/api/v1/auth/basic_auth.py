#!/usr/bin/env python3
"""Basic authentication
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract authorization from header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic'):
            return None
        token = authorization_header.split(' ')
        if len(token) < 2:
            return None
        return token[1]

    def decode_base64_authorization_header(self,
                                           authorization_header: str) -> str:
        """ decode base64 string
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None

        try:
            return base64.b64decode(authorization_header).decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """extract email and password
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        data = decoded_base64_authorization_header.split(':', 1)
        if len(data) < 2:
            return None, None
        return data[0], data[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """find and validate users credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            search_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in search_users:
            if user.is_valid_password(user_pwd):
                return user
            else:
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return current logged in user from auth header
        """
        token = self.authorization_header(request)
        base64token = self.extract_base64_authorization_header(token)
        decoded_token = self.decode_base64_authorization_header(base64token)
        user_email, user_pwd = self.extract_user_credentials(decoded_token)
        return self.user_object_from_credentials(user_email, user_pwd)
