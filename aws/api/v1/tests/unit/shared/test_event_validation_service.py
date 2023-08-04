import json
from unittest.mock import MagicMock

import pytest

from aws.api.v1.src.shared.services.event_validation_service import (
    AUTHORIZE_SUCCESSFUL,
    VALIDATION_SUCCESSFUL,
    EventValidator,
    InvalidTypeError,
    InvalidValueError,
    MissingParameterError,
    UnauthorizedError,
    ValidationErrorMessages,
)


def load_event(filename: str):
    with open(f"./aws/api/v1/events/shared/event_validation_service/{filename}", "r") as f:
        return json.load(f)


@pytest.fixture
def event(request):
    return load_event(request.param)


@pytest.fixture
def validator_with_mocked_logger(event):
    validator = EventValidator(event)
    validator.logger = MagicMock()
    return validator, validator.logger


@pytest.mark.parametrize("event", ["missing_query_string_param.json"], indirect=True)
def test_get_query_string_parameter_missing(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(MissingParameterError) as excinfo:
        validator.get_query_string_parameter(
            name="missing_param",
            optional=False,
            expected_type=str,
            allowed_values=None,
        )
    expected_message = ValidationErrorMessages.MISSING_PARAMETER.format(parameter="missing_param")
    assert str(excinfo.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", ["valid_event.json"], indirect=True)
def test_get_query_string_parameter_exists(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger

    assert validator.get_query_string_parameter("valid_param") == "value"
    mock_logger.info.assert_called_once_with(VALIDATION_SUCCESSFUL.format(parameter="valid_param"))


@pytest.mark.parametrize("event", ["invalid_query_string_param_type.json"], indirect=True)
def test_get_query_string_parameter_wrong_type(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidTypeError):
        validator.get_query_string_parameter("invalid_type_param", expected_type=int)
    expected_message = ValidationErrorMessages.INVALID_TYPE.format(
        parameter="invalid_type_param",
        actual="str",
        expected="int",
    )
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", ["valid_event.json"], indirect=True)
def test_get_query_string_parameter_not_in_allowed_values(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidValueError):
        validator.get_query_string_parameter(
            "valid_param",
            allowed_values=["other_value"],
        )
    expected_message = ValidationErrorMessages.PARAMETER_NOT_IN_SET.format(
        parameter="valid_param",
        value="value",
        allowed_values="['other_value']",
    )
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", ["missing_path_param.json"], indirect=True)
def test_get_path_parameter_missing(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(MissingParameterError):
        validator.get_path_parameter("missing_param")
    expected_message = ValidationErrorMessages.MISSING_PARAMETER.format(parameter="missing_param")
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", ["valid_event.json"], indirect=True)
def test_get_path_parameter_exists(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    assert validator.get_path_parameter("valid_param") == "value"


@pytest.mark.parametrize("event", ["invalid_path_param_type.json"], indirect=True)
def test_get_path_parameter_wrong_type(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidTypeError):
        validator.get_path_parameter("invalid_type_param", expected_type=str)
    expected_message = ValidationErrorMessages.INVALID_TYPE.format(
        parameter="invalid_type_param",
        actual="int",
        expected="str",
    )
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", ["valid_event.json"], indirect=True)
def test_get_path_parameter_not_in_allowed_values(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidValueError):
        validator.get_path_parameter(
            "valid_param",
            allowed_values=["other_value"],
        )
    expected_message = ValidationErrorMessages.PARAMETER_NOT_IN_SET.format(
        parameter="valid_param",
        value="value",
        allowed_values="['other_value']",
    )
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", ["missing_authorizer_param.json"], indirect=True)
def test_get_authorizer_parameter_missing(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(UnauthorizedError):
        validator.get_authorizer_parameter("missing_param")
    expected_message = ValidationErrorMessages.UNAUTHORIZED
    mock_logger.error.assert_any_call(expected_message)


@pytest.mark.parametrize("event", ["valid_event.json"], indirect=True)
def test_get_authorizer_parameter_exists(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    assert validator.get_authorizer_parameter("valid_param") == "value"
    mock_logger.info.assert_any_call(AUTHORIZE_SUCCESSFUL.format(parameter="valid_param"))