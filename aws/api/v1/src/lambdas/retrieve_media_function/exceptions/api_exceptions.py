from base_exceptions import CustomException
from constants.error_messages import INVALID_URL_MSG


class ObjectNotFoundError(CustomException):
    """Exception raised when an expected object is not found."""

    def __init__(self, message="Expected object was not found"):
        self.message = message
        super().__init__(message)


class InvalidURLError(TypeError):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, message=INVALID_URL_MSG):
        self.message = message
        super().__init__(self.message)
