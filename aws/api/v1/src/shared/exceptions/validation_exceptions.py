from typing import Any

from shared.constants.error_messages import ValidationErrorMessages

from .base_exceptions import CustomException


class MissingParameterError(CustomException):
    """Exception raised for missing parameter error."""

    def __init__(self, parameter: str):
        self.parameter = parameter
        self.message = ValidationErrorMessages.MISSING_PARAMETER.format(parameter=parameter)
        super().__init__(self.message)


class InvalidTypeError(CustomException):
    def __init__(self, parameter: str, actual: type, expected: type):
        super().__init__(
            ValidationErrorMessages.INVALID_TYPE.format(
                parameter=parameter,
                actual=actual,
                expected=expected,
            )
        )


class InvalidValueError(CustomException):
    def __init__(self, parameter: str, value: Any, allowed_values: Any):
        super().__init__(
            ValidationErrorMessages.MISSING_PARAMETER.format(
                parameter=parameter,
                value=value,
                allowed_values=allowed_values,
            )
        )


class UnauthorizedError(CustomException):
    """Exception raised for unauthorized access."""

    def __init__(self, message=ValidationErrorMessages.UNAUTHORIZED):
        self.message = message
        super().__init__(self.message)
