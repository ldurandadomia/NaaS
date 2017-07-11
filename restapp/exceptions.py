__author__ = "Laurent DURAND"

from werkzeug.exceptions import NotFound

class IntegrityConstraintViolation(Exception):
    """Exception Raised when a unicity constraint is violated"""
    def __init__(self, msg):
        self.message = msg


class MissingAttribute(Exception):
    """Exception Raised when some attribute is missing"""
    def __init__(self, msg):
        self.message = msg


class BadAttribute(Exception):
    """Exception Raised when some attribute is not supported or allowed"""
    def __init__(self, msg):
        self.message = msg