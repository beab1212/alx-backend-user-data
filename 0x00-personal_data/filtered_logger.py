#!/usr/bin/env python3
"""
PII(Personally Identifiable Information)
"""
import logging
import re
from typing import List
import mysql.connector
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for obfuscated in fields:
        message = re.sub(rf'{obfuscated}=.*?{separator}',
                         rf'{obfuscated}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter PII from log message """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ Create new logger object with specific config """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connects to mysql database """
    DB_HOST = os.environ.get('PERSONAL_DATA_DB_HOST')
    DB_USER = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    DB_PASSWORD = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    DB_NAME = os.environ.get('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(host=DB_HOST, user=DB_USER,
                                   password=DB_PASSWORD, database=DB_NAME)
