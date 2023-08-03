#!/usr/bin/env python3
"""Usage of regex to replace occurrences of certain values"""
import re
import logging
import csv


def filter_datum(fields, redaction, message, separator):
    """Returns log message obfuscated"""
    return re.sub(r'(' + '|'.join(fields) + r')=[^' + separator + r']*'
                  + separator, r'\1=' + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initializing the formatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting the fields"""
        for field in self.fields:
            record.msg = re.sub(rf'{field}=.*?;', rf'{field}={self.REDACTION};', record.msg)
        return super(RedactingFormatter, self).format(record) 


def get_logger() -> logging.Logger:
    """Get logger details"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger

PII_FIELDS = ("name", "email", "phone", "credit_card", "address")
