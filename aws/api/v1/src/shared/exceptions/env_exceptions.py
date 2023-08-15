from http import HTTPStatus
from typing import List

from shared.constants.logging_messages import EnvironmentMessages

from .exceptions import AppError


class EnvironmentError(AppError):
    """Base class for exceptions in environment variables."""

    def __init__(self, user_message, log_message, http_status, **log_args):
        super().__init__(user_message, log_message, http_status, log_args)


class EnvironmentVariableError(EnvironmentError):
    """Exception raised for errors in the environment variables."""

    def __init__(self, var_name: str):
        log_args = {"var_name": var_name}
        super().__init__(
            user_message=f"Environment variable '{var_name}' not set.",
            log_message=EnvironmentMessages.Error.ENV_VAR_NOT_SET.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class MissingEnvironmentVariableError(EnvironmentError):
    """Exception raised for missing environment variables."""

    def __init__(self, missing_vars: List[str]):
        log_args = {"missing_vars": ", ".join(missing_vars)}
        super().__init__(
            user_message=f"Missing environment variables: {', '.join(missing_vars)}.",
            log_message=EnvironmentMessages.Error.MISSING_ENV_VARS.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )
