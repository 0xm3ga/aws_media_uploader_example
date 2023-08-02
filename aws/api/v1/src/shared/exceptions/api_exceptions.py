from ..constants.error_messages import INVALID_URL_MSG, OBJECT_NOT_FOUND_MSG
from .base_exceptions import CustomException


class ObjectNotFoundError(CustomException):
    """Exception raised when an expected object is not found."""

    def __init__(self, message=OBJECT_NOT_FOUND_MSG):
        self.message = message
        super().__init__(message)


class InvalidURLError(TypeError):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, message=INVALID_URL_MSG):
        self.message = message
        super().__init__(self.message)
