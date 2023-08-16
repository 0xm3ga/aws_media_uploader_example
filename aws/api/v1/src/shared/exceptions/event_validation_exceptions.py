from http import HTTPStatus
from typing import Any, List, Optional

from shared.constants.logging_messages import HttpMessages, ValidationMessages
from shared.exceptions import AppError


class EventValidationError(AppError):
    """Base class for exceptions in Event Validation operations."""

    def __init__(
        self,
        user_message=HttpMessages.User.BAD_REQUEST,
        log_message=ValidationMessages.Error.GENERIC_ERROR,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        **log_args,
    ):
        super().__init__(
            user_message,
            log_message,
            http_status,
            log_args,
        )


class MissingParameterError(EventValidationError):
    """Exception raised for missing parameter error."""

    def __init__(self, param: str):
        log_args = {
            "param": param,
        }
        super().__init__(
            user_message=ValidationMessages.User.MISSING_PARAM.format(**log_args),
            log_message=ValidationMessages.Error.MISSING_PARAM.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class MissingAuthorizerError(EventValidationError):
    """Exception raised for unauthorized access."""

    def __init__(self, authorizer: str = "Authorizer"):
        log_args = {
            "authorizer": authorizer,
        }
        super().__init__(
            user_message=HttpMessages.User.UNAUTHORIZED,
            log_message=ValidationMessages.Error.MISSING_AUTHORIZER.format(**log_args),
            http_status=HTTPStatus.UNAUTHORIZED,
            **log_args,
        )


class MissingPathParamError(EventValidationError):
    """Exception raised when a required path parameter is missing."""

    def __init__(self, param: str):
        log_args = {
            "param": param,
        }
        super().__init__(
            user_message=ValidationMessages.User.MISSING_PATH_PARAM.format(**log_args),
            log_message=ValidationMessages.Error.MISSING_PATH_PARAM.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            **log_args,
        )


class MissingQueryStringParamError(EventValidationError):
    """Exception raised when a required query parameter is missing."""

    def __init__(self, param: str):
        log_args = {
            "param": param,
        }
        super().__init__(
            user_message=ValidationMessages.User.MISSING_QUERY_STR_PARAM.format(**log_args),
            log_message=ValidationMessages.Error.MISSING_QUERY_STR_PARAM.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            **log_args,
        )


class InvalidParamError(EventValidationError):
    """Raised when a provided parameter is invalid."""

    def __init__(self, param: str):
        log_args = {
            "param": param,
        }
        super().__init__(
            user_message=ValidationMessages.User.INVALID_PARAM_TYPE.format(**log_args),
            log_message=ValidationMessages.Error.INVALID_PARAM_TYPE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            **log_args,
        )


class InvalidParamTypeError(EventValidationError):
    """Raised when a provided parameter type is invalid."""

    def __init__(self, param: str, actual: type, allowed: Optional[List[type]] = None):
        log_args = {
            "param": param,
            "actual": actual,
            "allowed": allowed,
        }
        super().__init__(
            user_message=ValidationMessages.User.INVALID_PARAM_TYPE.format(**log_args),
            log_message=ValidationMessages.Error.INVALID_PARAM_TYPE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidParamValueError(EventValidationError):
    """Raised when a provided parameter value is invalid."""

    def __init__(self, param: str, actual: Any, allowed: Optional[List[Any]] = None):
        log_args = {
            "param": param,
            "actual": actual,
            "allowed": allowed,
        }
        super().__init__(
            user_message=ValidationMessages.User.INVALID_PARAM_VALUE.format(**log_args),
            log_message=ValidationMessages.Error.INVALID_PARAM_VALUE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )
