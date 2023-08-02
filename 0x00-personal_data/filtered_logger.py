#!/usr/bin/env python3
"""Usage of regex to replace occurrences of certain values"""
import re
import logging


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

    def __init__(self):
        """Initializing the formatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting the fields"""
        for field in self.fields:
            record.msg = re.sub(rf'{field}=.*?;', rf'{field}={self.REDACTION};', record.msg)
        return super(RedactingFormatter, self).format(record) 
