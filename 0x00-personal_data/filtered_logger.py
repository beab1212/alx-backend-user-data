#!/usr/bin/env python3
"""
PII(Personally Identifiable Information)
"""
import logging
import re
from mysql.connector import MySQLConnection
from os import getenv


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns the log message obfuscated
    """
    for obfuscated in fields:
        message = re.sub(rf'{obfuscated}=.*?{separator}',
                         rf'{obfuscated}={redaction}{separator}',
                         message)
    return message
