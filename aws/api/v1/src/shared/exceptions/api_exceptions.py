from shared.constants.logging_messages import S3Messages


class ObjectNotFoundError(Exception):
    """Exception raised when an expected object is not found."""

    def __init__(self, message=S3Messages.Error.OBJECT_NOT_FOUND):
        self.message = message
        super().__init__(message)


class InvalidURLError(TypeError):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, message=S3Messages.Error.INVALID_URL):
        self.message = message
        super().__init__(self.message)
