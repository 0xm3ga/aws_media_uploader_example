import json
import logging
from http import HTTPStatus
from typing import Any, Dict

from shared.constants.logging_messages import ApiMessages, GeneralMessages

logger = logging.getLogger(__name__)


class ApiBaseService:
    @classmethod
    def create_response(cls, status_code: HTTPStatus, message: Any) -> Dict[str, Any]:
        """Creates a standard HTTP response."""
        try:
            message = json.dumps(message)
        except TypeError as e:
            error_message = GeneralMessages.Error.JSON_SERIALIZATION_ERROR.format(error=str(e))
            logger.error(error_message)
            raise ValueError(error_message) from None

        logger.info(
            ApiMessages.Info.RESPONSE_CREATED.format(
                status=status_code.value,
                message=message,
            )
        )
        return {
            "statusCode": status_code.value,
            "body": message,
        }

    @classmethod
    def create_redirect(cls, status_code: HTTPStatus, location: str) -> Dict[str, Any]:
        """Creates a standard HTTP redirect response."""
        logger.info(
            ApiMessages.Info.REDIRECT_CREATED.format(
                status=status_code.value,
                location=str(location),
            )
        )
        return {
            "statusCode": status_code.value,
            "headers": {"Location": str(location)},
        }
