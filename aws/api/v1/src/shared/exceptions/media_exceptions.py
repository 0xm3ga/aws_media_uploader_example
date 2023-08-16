from http import HTTPStatus
from typing import Optional

from shared.constants.logging_messages import HttpMessages, MediaMessages, ProcessingMessages
from shared.exceptions import AppError


class MediaError(AppError):
    """Base class for exceptions in media operations."""

    def __init__(
        self,
        user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
        log_message=MediaMessages.Error.GENERIC_ERROR,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        **log_args,
    ):
        super().__init__(
            user_message,
            log_message,
            http_status,
            log_args,
        )


class InvalidMediaTypeError(MediaError):
    """Exception raised for invalid media types."""

    def __init__(self, media_type: str = ""):
        log_args = {
            "media_type": media_type,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=MediaMessages.Error.INVALID_MEDIA_TYPE,
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidExtensionError(MediaError):
    """Exception raised for invalid extensions."""

    def __init__(self, extension: Optional[str] = ""):
        log_args = {
            "extension": extension,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=MediaMessages.Error.INVALID_EXTENSION.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidContentTypeError(MediaError):
    """Exception raised for invalid content types."""

    def __init__(self, content_type: str):
        log_args = {
            "content_type": content_type,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=ProcessingMessages.Error.INVALID_CONTENT_TYPE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidSizeError(MediaError):
    """Raised when an invalid or unsupported size is encountered."""

    def __init__(self, m):
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=MediaMessages.Error.INVALID_SIZE,
            http_status=HTTPStatus.BAD_REQUEST,
        )


class InvalidAspectRatioError(MediaError):
    """Raised when an invalid or unsupported aspect ratio is encountered."""

    def __init__(self):
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=MediaMessages.Error.INVALID_ASPECT_RATIO,
            http_status=HTTPStatus.BAD_REQUEST,
        )
