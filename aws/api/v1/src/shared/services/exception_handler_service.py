import logging
from http import HTTPStatus

from shared.constants.logging_messages import GeneralMessages
from shared.exceptions.base_exceptions import CustomException

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ExceptionHandler:
    @staticmethod
    def handle_exception(e: Exception) -> CustomException:
        if not isinstance(e, CustomException):
            e = CustomException(
                user_message=GeneralMessages.Error.UNEXPECTED_ERROR,
                log_message=str(e),
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        ExceptionHandler.log_error(e)
        return e

    @staticmethod
    def log_error(error: CustomException):
        logger.error(
            GeneralMessages.Error.LOG_ERROR_FORMAT.format(
                error_type=type(error).__name__,
                message=error.log_message,
            )
        )
