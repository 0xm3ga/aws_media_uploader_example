from constants.error_messages import INVALID_FORMAT_MSG, INVALID_SIZE_MSG
from exceptions import CustomException


class InvalidImageFormatError(CustomException):
    """Exception raised when an unsupported image format is encountered."""

    def __init__(self, extension: str):
        super().__init__(INVALID_FORMAT_MSG.format(extension))


class InvalidImageSizeError(CustomException):
    """Exception raised when an unsupported image size is encountered."""

    def __init__(self, size: str):
        super().__init__(INVALID_SIZE_MSG.format(size))
