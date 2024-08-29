#!/usr/bin/env python3
"""
PII(Personally Identifiable Information)
"""
import logging
from logging import StreamHandler
import re
from typing import List
from mysql.connector import MySQLConnection
from os import getenv


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


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
    """ create new logger object with specific config """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> MySQLConnection:
    """ return mysql connector """
    db_username = getenv('PERSONAL_DATA_DB_USERNAME', default='root')
    db_password = getenv('PERSONAL_DATA_DB_PASSWORD', default='')
    db_host = getenv('PERSONAL_DATA_DB_HOST', default='localhost')
    db = getenv('PERSONAL_DATA_DB_NAME', 'my_db')
    return MySQLConnection(user=db_username, password=db_password,
                           host=db_host, database=db)
