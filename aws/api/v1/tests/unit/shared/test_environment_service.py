import os
from unittest.mock import patch

import pytest

from aws.api.v1.src.shared.constants.error_messages.env_error_messages import (
    EnvironmentErrorMessages,
)
from aws.api.v1.src.shared.services.environment_service import (
    Environment,
    EnvironmentVariableError,
    MissingEnvironmentVariableError,
)


@pytest.fixture
def mock_logger():
    with patch("aws.api.v1.src.shared.services.environment_service.logger") as _mock:
        yield _mock


def test_fetch_variable_existing(mock_logger):
    with patch.dict(os.environ, {"EXISTING_VAR": "test_value"}):
        env = Environment([])
        assert env.fetch_variable("EXISTING_VAR") == "test_value"


def test_fetch_variable_non_existing(mock_logger):
    env = Environment([])
    with pytest.raises(EnvironmentVariableError) as excinfo:
        env.fetch_variable("NON_EXISTING_VAR")
    expected_message = EnvironmentErrorMessages.ENV_VAR_NOT_SET.format(var_name="NON_EXISTING_VAR")
    assert str(excinfo.value) == expected_message
    mock_logger.error.assert_called_once()


def test_fetch_required_variables_all_exist(mock_logger):
    with patch.dict(os.environ, {"EXISTING_VAR": "test_value"}):
        env = Environment(["EXISTING_VAR"])
        env.fetch_required_variables()
        mock_logger.error.assert_not_called()


@pytest.mark.parametrize(
    "existing_vars, required_vars, missing_vars",
    [
        (["EXISTING_VAR"], ["EXISTING_VAR", "NON_EXISTING_VAR"], ["NON_EXISTING_VAR"]),
        (
            [],
            ["NON_EXISTING_VAR_1", "NON_EXISTING_VAR_2"],
            ["NON_EXISTING_VAR_1", "NON_EXISTING_VAR_2"],
        ),
        (["IRRELEVANT_VAR"], ["NON_EXISTING_VAR"], ["NON_EXISTING_VAR"]),
    ],
)
def test_fetch_required_variables_missing(mock_logger, existing_vars, required_vars, missing_vars):
    with patch.dict(os.environ, {var: "test_value" for var in existing_vars}):
        env = Environment(required_vars)
        with pytest.raises(MissingEnvironmentVariableError) as excinfo:
            env.fetch_required_variables()
        expected_message = EnvironmentErrorMessages.MISSING_ENV_VARS.format(
            missing_vars=", ".join(missing_vars)
        )
        assert str(excinfo.value) == expected_message
        assert mock_logger.error.call_count == len(missing_vars) + 1
