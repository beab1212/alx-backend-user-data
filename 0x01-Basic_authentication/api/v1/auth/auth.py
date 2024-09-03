#!/usr/bin/env python3
"""authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check whether or not path exist in excluded_path list
           with slash tolerant
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path[-1] != '/' and path + '/' in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and \
               path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """extract 'Authorization' header from request
        """
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """doc
        """
        return None
