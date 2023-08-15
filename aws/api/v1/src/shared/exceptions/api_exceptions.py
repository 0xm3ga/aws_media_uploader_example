from http import HTTPStatus

from shared.constants.logging_messages import S3Messages

from .exceptions import AppError


class ObjectNotFoundError(AppError):
    """Exception raised when an expected object is not found."""

    def __init__(self, object_name: str):
        log_args = {"object_name": object_name}
        super().__init__(
            user_message=f"Object '{object_name}' not found.",
            log_message=S3Messages.Error.OBJECT_NOT_FOUND.format(**log_args),
            http_status=HTTPStatus.NOT_FOUND,  # Assuming HTTPStatus has been imported
            log_args=log_args,
        )


class InvalidURLError(AppError):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, url: str, reason: str):
        log_args = {"url": url, "reason": reason}
        super().__init__(
            user_message="Invalid URL.",
            log_message=S3Messages.Error.INVALID_URL.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,  # Assuming HTTPStatus has been imported
            log_args=log_args,
        )
