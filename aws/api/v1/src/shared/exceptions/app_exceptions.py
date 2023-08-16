import json
import logging
from http import HTTPStatus
from typing import Optional

from shared.constants.logging_messages import GeneralMessages, HttpMessages

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
        return {
            "statusCode": self.http_status,
            "body": json.dumps({"message": self.user_message}),
        }


class FeatureNotImplementedError(AppError):
    """Raised when a feature is not yet implemented."""

    def __init__(self, feature_name: str):
        log_args = {
            "feature_name": feature_name,
        }
        super().__init__(
            user_message=HttpMessages.User.INTERNAL_SERVER_ERROR,
            log_message=GeneralMessages.Error.FEATURE_NOT_IMPLEMENTED.format(**log_args),
            http_status=HTTPStatus.NOT_IMPLEMENTED,
            log_args=log_args,
        )
