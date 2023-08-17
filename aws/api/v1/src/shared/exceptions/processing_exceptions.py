from http import HTTPStatus

from shared.constants.logging_messages import HttpMessages, MediaMessages, ProcessingMessages
from shared.exceptions import AppError


class ProcessingError(AppError):
    """Base class for exceptions related to media processing."""

    def __init__(self, user_message, log_message, http_status, **log_args):
        super().__init__(
            user_message,
            log_message,
            http_status,
            log_args,
        )


class UnsupportedExtensionError(ProcessingError):
    """Exception raised when an unsupported file extension is encountered."""

    def __init__(self, extension: str):
        log_args = {
            "extension": extension,
        }
        super().__init__(
            user_message=f"Unsupported file extension: {extension}",
            log_message=MediaMessages.Error.UNSUPPORTED_EXTENSION.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class UnsupportedSizeError(ProcessingError):
    """Exception raised when an unsupported size is encountered."""

    def __init__(self, size: str):
        log_args = {"size": size}
        super().__init__(
            user_message=f"Unsupported size: {size}",
            log_message=MediaMessages.Error.UNSUPPORTED_SIZE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class MediaProcessingError(ProcessingError):
    """Exception raised during file processing."""

    def __init__(self):
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=ProcessingMessages.Error.GENERIC_ERROR,
            http_status=HTTPStatus.BAD_REQUEST,
        )
