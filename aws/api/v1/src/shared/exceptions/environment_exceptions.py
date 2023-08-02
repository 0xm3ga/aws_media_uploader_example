from shared.constants.error_messages import ENV_VAR_NOT_SET_MSG, MISSING_ENV_VARS_MSG

from .base_exceptions import CustomException


class EnvironmentVariableError(CustomException):
    """Exception raised for errors in the environment variables."""

    def __init__(self, var_name: str):
        self.var_name = var_name
        self.message = ENV_VAR_NOT_SET_MSG.format(var_name=self.var_name)
        super().__init__(self.var_name)


class MissingEnvironmentVariableError(CustomException):
    """Exception raised for missing environment variables."""

    def __init__(self, missing_vars: list):
        self.missing_vars = missing_vars
        self.message = MISSING_ENV_VARS_MSG.format(missing_vars=", ".join(missing_vars))
        super().__init__(self.missing_vars)
