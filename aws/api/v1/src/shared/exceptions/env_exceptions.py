from shared.constants.logging_messages import EnvironmentMessages

from .base_exceptions import CustomException


class EnvironmentVariableError(CustomException):
    """Exception raised for errors in the environment variables."""

    def __init__(self, var_name: str):
        self.var_name = var_name
        self.message = EnvironmentMessages.Error.ENV_VAR_NOT_SET.format(var_name=self.var_name)
        super().__init__(self.message)


class MissingEnvironmentVariableError(CustomException):
    """Exception raised for missing environment variables."""

    def __init__(self, missing_vars):
        self.missing_vars = missing_vars
        self.message = EnvironmentMessages.Error.MISSING_ENV_VARS.format(
            missing_vars=", ".join(missing_vars)
        )
        super().__init__(self.message)
