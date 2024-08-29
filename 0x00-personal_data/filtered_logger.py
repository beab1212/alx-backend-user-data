#!/usr/bin/env python3
"""
PII(Personally Identifiable Information)
"""
import logging
import re
from typing import List
from mysql.connector import MySQLConnection
from os import getenv


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for obfuscated in fields:
        message = re.sub(rf'{obfuscated}=.*?{separator}',
                         rf'{obfuscated}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def filter_datum(self, field: str, redaction: str,
                     message: str, separator: str) -> str:
        """
        Returns the log message obfuscated
        """
        return re.sub(rf'{field}=.*?{separator}',
                      rf'{field}={redaction}{separator}',
                      message)

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter PII from log message
        """
        for field in self.fields:
            record.msg = self.filter_datum(field, self.REDACTION,
                                           record.msg, self.SEPARATOR)
        return super().format(record)
