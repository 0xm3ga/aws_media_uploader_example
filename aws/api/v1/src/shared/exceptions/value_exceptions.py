from http import HTTPStatus

from shared.constants.logging_messages import MediaMessages, ProcessingMessages
from shared.exceptions import AppError


class InvalidImageFormatError(AppError):
    """Exception raised when an unsupported image format is encountered."""

    def __init__(self, extension: str):
        log_args = {"extension": extension}
        super().__init__(
            user_message=f"Unsupported image format: {extension}",
            log_message=ProcessingMessages.Error.UNSUPPORTED_EXTENSION.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidImageSizeError(AppError):
    """Exception raised when an unsupported image size is encountered."""

    def __init__(self, size: str):
        log_args = {"size": size}
        super().__init__(
            user_message=f"Unsupported image size: {size}",
            log_message=ProcessingMessages.Error.UNSUPPORTED_SIZE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidMediaTypeError(AppError):
    """Exception raised for invalid media types."""

    def __init__(self, message="Invalid media type"):
        super().__init__(
            user_message=message, log_message=message, http_status=HTTPStatus.BAD_REQUEST
        )


class InvalidExtensionError(AppError):
    """Exception raised for invalid extensions."""

    def __init__(self, message="Invalid extension"):
        super().__init__(
            user_message=message, log_message=message, http_status=HTTPStatus.BAD_REQUEST
        )


class InvalidContentTypeError(AppError):
    """Exception raised for invalid content types."""

    def __init__(self, content_type: str):
        log_args = {"content_type": content_type}
        super().__init__(
            user_message=f"Invalid content type: {content_type}",
            log_message=ProcessingMessages.Error.INVALID_CONTENT_TYPE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


# Media size
class MediaSizeException(AppError):
    """
    Base exception for all media size related errors.
    This can be expanded upon in the future if needed.
    """

    pass


class InvalidSizeError(MediaSizeException):
    """Raised when an invalid or unsupported size is encountered."""

    def __init__(self, message=MediaMessages.Error.INVALID_SIZE):
        super().__init__(
            user_message=message, log_message=message, http_status=HTTPStatus.BAD_REQUEST
        )


class InvalidAspectRatioError(MediaSizeException):
    """Raised when an invalid or unsupported aspect ratio is encountered."""

    def __init__(self, message=MediaMessages.Error.INVALID_ASPECT_RATIO):
        super().__init__(
            user_message=message, log_message=message, http_status=HTTPStatus.BAD_REQUEST
        )
