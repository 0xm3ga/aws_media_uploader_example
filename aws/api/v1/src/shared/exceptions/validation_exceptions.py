from typing import Any

from shared.constants import error_messages as em


class MissingParameterError(Exception):
    def __init__(self, parameter: str):
        super().__init__(em.MISSING_PARAMETER_ERROR_MSG.format(parameter=parameter))


class InvalidTypeError(Exception):
    def __init__(self, parameter: str, actual: type, expected: type):
        super().__init__(
            em.INVALID_TYPE_ERROR_MSG.format(
                parameter=parameter,
                actual=actual,
                expected=expected,
            )
        )


class InvalidValueError(Exception):
    def __init__(self, parameter: str, value: Any, allowed_values: Any):
        super().__init__(
            em.PARAMETER_NOT_IN_SET_ERROR_MSG.format(
                parameter=parameter,
                value=value,
                allowed_values=allowed_values,
            )
        )


class UnauthorizedError(Exception):
    """Exception raised for unauthorized access."""

    def __init__(self, message=em.UNAUTHORIZED_ERROR_MSG):
        self.message = message
        super().__init__(self.message)
