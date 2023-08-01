from constants import error_messages as em
from exceptions import CustomException


class InvalidImageFormatError(CustomException):
    """Exception raised when an unsupported image format is encountered."""

    def __init__(self, extension: str):
        super().__init__(em.INVALID_FORMAT_MSG.format(extension))


class InvalidImageSizeError(CustomException):
    """Exception raised when an unsupported image size is encountered."""

    def __init__(self, size: str):
        super().__init__(em.INVALID_SIZE_MSG.format(size))
