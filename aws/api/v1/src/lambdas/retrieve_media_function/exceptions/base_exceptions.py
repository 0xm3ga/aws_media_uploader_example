# exceptions/base_exceptions.py


class CustomException(Exception):
    """Base class for other exceptions"""

    def __init__(self, message, *args):
        self.message = message
        self.args = args
        super().__init__(message, *args)

    def __str__(self):
        return self.message
