from shared.constants.logging_messages import MediaMessages, ProcessingMessages

from .base_exceptions import CustomException


class InvalidImageFormatError(CustomException):
    """Exception raised when an unsupported image format is encountered."""

    def __init__(self, extension: str):
        super().__init__(ProcessingMessages.Error.UNSUPPORTED_EXTENSION.format(extension))


class InvalidImageSizeError(CustomException):
    """Exception raised when an unsupported image size is encountered."""

    def __init__(self, size: str):
        super().__init__(ProcessingMessages.Error.UNSUPPORTED_SIZE.format(size))


class InvalidMediaTypeError(ValueError):
    pass


class InvalidExtensionError(ValueError):
    pass


class InvalidContentTypeError(ValueError):
    def __init__(self, content_type: str):
        self.content_type = content_type
        self.message = ProcessingMessages.Error.INVALID_CONTENT_TYPE.format(
            content_type=content_type
        )
        super().__init__(self.message)


# Media size
class MediaSizeException(Exception):
    """
    Base exception for all media size related errors.
    This can be expanded upon in the future if needed.
    """

    pass


class InvalidSizeError(MediaSizeException):
    """Raised when an invalid or unsupported size is encountered."""

    def __init__(self, message=MediaMessages.Error.INVALID_SIZE):
        super().__init__(message)


class InvalidAspectRatioError(MediaSizeException):
    """Raised when an invalid or unsupported aspect ratio is encountered."""

    def __init__(self, message=MediaMessages.Error.INVALID_ASPECT_RATIO):
        super().__init__(message)
