#!/usr/bin/env python3
"""Usage of regex to replace occurrences of certain values"""
import re
import logging
import csv
import mysql.connector
import os
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filters a log line"""
    return re.sub(r'(' + '|'.join(fields) + r')=[^' + separator + r']*'
                  + separator, r'\1=' + redaction + separator, message)


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a database"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_username,
            password=db_password,
            database=db_name,
    )
    return connection


def main():
    """Logs the information about user records in a table"""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


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
            record.msg = re.sub(rf'{field}=.*?;',
                                rf'{field}={self.REDACTION};', record.msg)
        return super(RedactingFormatter, self).format(record)
