from http import HTTPStatus
from typing import Any, Optional

from shared.constants.logging_messages import ValidationMessages
from shared.exceptions import AppError


class MissingParameterError(AppError):
    """Exception raised for missing parameter error."""

    def __init__(self, parameter: str):
        log_args = {"parameter": parameter}
        super().__init__(
            user_message=f"Missing parameter: {parameter}",
            log_message=ValidationMessages.Error.MISSING_PARAMETER.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidTypeError(AppError):
    def __init__(self, parameter: str, actual: type, expected: type):
        log_args = {"parameter": parameter, "actual": actual, "expected": expected}
        super().__init__(
            user_message=f"Invalid type for parameter '{parameter}'.\
                Expected '{expected}', got '{actual}'.",
            log_message=ValidationMessages.Error.INVALID_TYPE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidValueError(AppError):
    def __init__(self, parameter: str, value: Any, allowed_values: Optional[Any] = ""):
        log_args = {"parameter": parameter, "value": value, "allowed_values": allowed_values}
        super().__init__(
            user_message=f"Invalid value '{value}' for parameter '{parameter}'.\
                  Allowed values: {allowed_values}",
            log_message=ValidationMessages.Error.MISSING_PARAMETER.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class UnauthorizedError(AppError):
    """Exception raised for unauthorized access."""

    def __init__(self, message=ValidationMessages.Error.UNAUTHORIZED):
        super().__init__(
            user_message=message, log_message=message, http_status=HTTPStatus.UNAUTHORIZED
        )
