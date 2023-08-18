from http import HTTPStatus

from shared.constants.logging_messages import HttpMessages, RdsMessages
from shared.exceptions import AppError


class RdsError(AppError):
    """Base class for exceptions in AWS S3 operations."""

    def __init__(
        self,
        user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
        log_message=RdsMessages.Error.GENERIC_ERROR,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        **log_args,
    ):
        super().__init__(
            user_message,
            log_message,
            http_status,
            log_args,
        )


class RdsCommunicationError(RdsError):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        log_args = {
            "error": error,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=RdsMessages.Error.RDS_COMMUNICATION_ERROR.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )


class MissingRequiredRDSVariablesError(RdsError):
    """Exception raised when required variables are missing in the response from RDS."""

    def __init__(self, error: str = ""):
        log_args = {
            "error": error,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=RdsMessages.Error.MISSING_VARIABLES_IN_RESPONSE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )
