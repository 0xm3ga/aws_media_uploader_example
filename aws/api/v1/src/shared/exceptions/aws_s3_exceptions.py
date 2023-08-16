from http import HTTPStatus

from shared.constants.logging_messages import HttpMessages, S3Messages
from shared.exceptions import AppError


class S3Error(AppError):
    """Base class for exceptions in AWS S3 operations."""

    def __init__(
        self,
        user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
        log_message=S3Messages.Error.GENERIC_ERROR,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        **log_args
    ):
        super().__init__(
            user_message,
            log_message,
            http_status,
            log_args,
        )


class ObjectNotFoundError(S3Error):
    """Exception raised when an expected object is not found."""

    def __init__(self, key: str, bucket: str):
        log_args = {
            "key": key,
            "bucket": bucket,
        }
        super().__init__(
            user_message=HttpMessages.User.OBJECT_NOT_FOUND,
            log_message=S3Messages.Error.OBJECT_NOT_FOUND.format(**log_args),
            http_status=HTTPStatus.NOT_FOUND,
            log_args=log_args,
        )


class PresignedUrlGenerationError(S3Error):
    """Raised when there is an error generating a presigned URL."""

    def __init__(self, error: str):
        log_args = {
            "error": error,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=S3Messages.Error.FAILED_TO_GENERATE_PRESIGNED_URL.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )


class InvalidURLError(S3Error):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, url: str):
        log_args = {
            "url": url,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=S3Messages.Error.INVALID_URL.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )
