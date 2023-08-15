from http import HTTPStatus

from shared.constants.logging_messages import S3Messages

from .exceptions import AppError


class BaseS3Error(AppError):
    """Base class for exceptions in AWS S3 operations."""

    def __init__(self, user_message, log_message, http_status, **log_args):
        super().__init__(user_message, log_message, http_status, log_args)


class PresignedUrlGenerationError(BaseS3Error):
    """Raised when there is an error generating a presigned URL."""

    def __init__(self, error: str):
        log_args = {"error": error}
        super().__init__(
            user_message="Failed to generate presigned URL.",
            log_message=S3Messages.Error.FAILED_TO_GENERATE_PRESIGNED_URL.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,  # Assuming HTTPStatus has been imported
            log_args=log_args,
        )
