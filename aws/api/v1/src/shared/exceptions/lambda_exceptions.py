from http import HTTPStatus

from shared.constants.logging_messages import HttpMessages, LambdaMessages
from shared.exceptions import AppError


class LambdaError(AppError):
    """Base class for exceptions in AWS Lamdba operations."""

    def __init__(
        self,
        user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
        log_message=LambdaMessages.Error.GENERIC_ERROR,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        **log_args,
    ):
        super().__init__(
            user_message,
            log_message,
            http_status,
            log_args,
        )


class LambdaInvocationError(LambdaError):
    """Raised when there is an error invoking the Lambda function."""

    def __init__(self, error=""):
        log_args = {
            "error": error,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=LambdaMessages.Error.ERROR_INVOKING_LAMBDA.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )


class LambdaResponseProcessingError(LambdaError):
    """Raised when there is an error processing the Lambda function response."""

    def __init__(self, error=""):
        log_args = {
            "error": error,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=LambdaMessages.Error.ERROR_PROCESSING_RESPONSE.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )
