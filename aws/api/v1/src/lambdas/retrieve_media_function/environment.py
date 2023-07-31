import logging
import os
from typing import List

from exceptions import (
    ENV_VAR_NOT_SET_MSG,
    MISSING_ENV_VARS_MSG,
    EnvironmentVariableError,
    MissingEnvironmentVariableError,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Environment:
    def __init__(self, required_vars: List[str]):
        self.required_vars = required_vars

    def fetch_variable(self, variable_name: str) -> str:
        """Fetch an environment variable."""
        var_value = os.environ.get(variable_name)
        if var_value is None:
            logger.error(ENV_VAR_NOT_SET_MSG.format(var_name=variable_name))
            raise EnvironmentVariableError(variable_name)
        return var_value

    def fetch_required_variables(self):
        missing_vars = []
        for var in self.required_vars:
            try:
                self.fetch_variable(var)
            except EnvironmentVariableError:
                missing_vars.append(var)
                logger.error(MISSING_ENV_VARS_MSG.format(var))

        if missing_vars:
            raise MissingEnvironmentVariableError(missing_vars)
