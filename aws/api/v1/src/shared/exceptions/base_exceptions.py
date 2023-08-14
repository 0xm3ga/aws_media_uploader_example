from http import HTTPStatus

from shared.constants.logging_messages import GeneralMessages


class CustomException(Exception):
    def __init__(
        self,
        user_message=GeneralMessages.Error.UNEXPECTED_ERROR_MESSAGE,
        log_message=GeneralMessages.Error.GENERIC_LOG_MESSAGE,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(log_message)
        self.user_message = user_message
        self.log_message = log_message
        self.http_status = http_status
