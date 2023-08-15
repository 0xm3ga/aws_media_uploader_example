from http import HTTPStatus

from shared.constants.logging_messages import RdsMessages
from shared.exceptions import AppError


class RDSCommunicationError(AppError):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        log_args = {"error": error}
        super().__init__(
            user_message=f"Failed to communicate with RDS: {error}",
            log_message=RdsMessages.Error.RDS_COMMUNICATION_ERROR.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )
