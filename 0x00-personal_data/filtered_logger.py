#!/usr/bin/env python3
"""
Returns the log message obfuscated
"""
import re
from typing import List
import logging


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
        """Formats a log message"""
        log_msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_msg,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return a log message
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing which
        character is separating all fields in the log line (message)
    Returns:
        An obuscated log message
    """
    for field in fields:
        pattern = r'{0}={1}(?={2}|$)'.format(
            field, r'[^{0}]*?'.format(separator), re.escape(separator))
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
