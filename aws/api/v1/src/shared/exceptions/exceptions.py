import json
import logging
from http import HTTPStatus
from typing import Optional

from shared.constants.logging_messages import GeneralMessages

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Custom exception class for application-specific errors."""

    def __init__(
        self,
        user_message=GeneralMessages.Error.UNEXPECTED_ERROR_MESSAGE,
        log_message=GeneralMessages.Error.GENERIC_LOG_MESSAGE,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        log_args: Optional[dict] = None,
    ):
        self.user_message = user_message
        self.log_message = log_message.format(**(log_args or {}))
        self.http_status = http_status
        super().__init__(self.log_message)
        self.log_error()

    def log_error(self) -> None:
        """Log the error message."""
        logger.error(f"{self.log_message}")

    def to_dict(self) -> dict:
        """Convert the error to a dictionary representation."""
        return {"statusCode": self.http_status, "body": json.dumps({"message": self.user_message})}


class CustomError(AppError):
    pass
