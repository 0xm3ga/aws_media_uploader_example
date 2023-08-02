from typing import Any

from shared.constants.error_messages import (
    INVALID_TYPE_ERROR_MSG,
    MISSING_PARAMETER_ERROR_MSG,
    PARAMETER_NOT_IN_SET_ERROR_MSG,
    UNAUTHORIZED_ERROR_MSG,
)

from .base_exceptions import CustomException


class MissingParameterError(CustomException):
    def __init__(self, parameter: str):
        super().__init__(MISSING_PARAMETER_ERROR_MSG.format(parameter=parameter))


class InvalidTypeError(CustomException):
    def __init__(self, parameter: str, actual: type, expected: type):
        super().__init__(
            INVALID_TYPE_ERROR_MSG.format(
                parameter=parameter,
                actual=actual,
                expected=expected,
            )
        )


class InvalidValueError(CustomException):
    def __init__(self, parameter: str, value: Any, allowed_values: Any):
        super().__init__(
            PARAMETER_NOT_IN_SET_ERROR_MSG.format(
                parameter=parameter,
                value=value,
                allowed_values=allowed_values,
            )
        )


class UnauthorizedError(CustomException):
    """Exception raised for unauthorized access."""

    def __init__(self, message=UNAUTHORIZED_ERROR_MSG):
        self.message = message
        super().__init__(self.message)
