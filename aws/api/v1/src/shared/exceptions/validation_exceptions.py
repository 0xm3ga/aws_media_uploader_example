from typing import Any, Optional

from shared.constants.logging_messages import ValidationMessages

from .base_exceptions import CustomException


class MissingParameterError(CustomException):
    """Exception raised for missing parameter error."""

    def __init__(self, parameter: str):
        self.parameter = parameter
        self.message = ValidationMessages.Error.MISSING_PARAMETER.format(parameter=parameter)
        super().__init__(self.message)


class InvalidTypeError(CustomException):
    def __init__(self, parameter: str, actual: type, expected: type):
        super().__init__(
            ValidationMessages.Error.INVALID_TYPE.format(
                parameter=parameter,
                actual=actual,
                expected=expected,
            )
        )


class InvalidValueError(CustomException):
    def __init__(self, parameter: str, value: Any, allowed_values: Optional[Any] = ""):
        super().__init__(
            ValidationMessages.Error.MISSING_PARAMETER.format(
                parameter=parameter,
                value=value,
                allowed_values=allowed_values,
            )
        )


class UnauthorizedError(CustomException):
    """Exception raised for unauthorized access."""

    def __init__(self, message=ValidationMessages.Error.UNAUTHORIZED):
        self.message = message
        super().__init__(self.message)
