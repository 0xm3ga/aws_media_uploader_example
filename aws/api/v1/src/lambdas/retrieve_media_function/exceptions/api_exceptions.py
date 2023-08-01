from base_exceptions import CustomException
from constants import error_messages as em


class ObjectNotFoundError(CustomException):
    """Exception raised when an expected object is not found."""

    def __init__(self, message=em.OBJECT_NOT_FOUND_MSG):
        self.message = message
        super().__init__(message)


class InvalidURLError(TypeError):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, message=em.INVALID_URL_MSG):
        self.message = message
        super().__init__(self.message)
