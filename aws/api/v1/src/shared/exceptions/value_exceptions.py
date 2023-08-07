from shared.constants.error_messages import MediaErrorMessages, ProcessingErrorMessages

from .base_exceptions import CustomException


class InvalidImageFormatError(CustomException):
    """Exception raised when an unsupported image format is encountered."""

    def __init__(self, extension: str):
        super().__init__(ProcessingErrorMessages.UNSUPPORTED_EXTENSION.format(extension))


class InvalidImageSizeError(CustomException):
    """Exception raised when an unsupported image size is encountered."""

    def __init__(self, size: str):
        super().__init__(ProcessingErrorMessages.UNSUPPORTED_SIZE.format(size))


class InvalidMediaTypeError(ValueError):
    pass


class InvalidExtensionError(ValueError):
    pass


class InvalidContentTypeError(ValueError):
    pass


# Media size
class MediaSizeException(Exception):
    """
    Base exception for all media size related errors.
    This can be expanded upon in the future if needed.
    """

    pass


class InvalidSizeError(MediaSizeException):
    """Raised when an invalid or unsupported size is encountered."""

    def __init__(self, message=MediaErrorMessages.INVALID_SIZE):
        super().__init__(message)


class InvalidAspectRatioError(MediaSizeException):
    """Raised when an invalid or unsupported aspect ratio is encountered."""

    def __init__(self, message=MediaErrorMessages.INVALID_ASPECT_RATIO):
        super().__init__(message)
