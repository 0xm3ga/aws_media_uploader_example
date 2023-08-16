import json
from unittest.mock import MagicMock

import pytest

from aws.api.v1.src.shared.services.event_validation_service import (
    EventValidator,
    InvalidParamTypeError,
    InvalidParamValueError,
    MissingAuthorizerError,
    MissingParameterError,
    ValidationMessages,
)


def load_event(filename: str):
    with open(f"./aws/api/v1/events/shared/event_validation_service/{filename}", "r") as f:
        return json.load(f)


# ===================== FIXTURES =====================
@pytest.fixture
def event(request):
    return load_event(request.param)


@pytest.fixture
def validator_with_mocked_logger(event):
    validator = EventValidator(event)
    validator.logger = MagicMock()
    return validator, validator.logger


# ====== CONSTANTS FOR PARAMETRIZATION ============================================
EVENT_NAMES = {
    "MISSING_QUERY": "missing_query_string_param.json",
    "VALID": "valid_event.json",
    "INVALID_QUERY_TYPE": "invalid_query_string_param_type.json",
    "MISSING_PATH": "missing_path_param.json",
    "INVALID_PATH_TYPE": "invalid_path_param_type.json",
    "MISSING_AUTHORIZER": "missing_authorizer_param.json",
}


# ====== TESTS: Query String Parameter ============================================
@pytest.mark.parametrize("event", [EVENT_NAMES["MISSING_QUERY"]], indirect=True)
def test_get_query_string_parameter_missing(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(MissingParameterError) as excinfo:
        validator.get_query_string_parameter(
            name="missing_param",
            optional=False,
            expected_type=str,
            allowed_values=None,
        )
    expected_message = ValidationMessages.Error.MISSING_PARAMETER.format(parameter="missing_param")
    assert str(excinfo.value) == expected_message
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", [EVENT_NAMES["VALID"]], indirect=True)
def test_get_query_string_parameter_exists(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger

    assert validator.get_query_string_parameter("valid_param") == "value"
    mock_logger.info.assert_called_once_with(
        ValidationMessages.Info.VALIDATION_SUCCESSFUL.format(parameter="valid_param")
    )


@pytest.mark.parametrize("event", [EVENT_NAMES["INVALID_QUERY_TYPE"]], indirect=True)
def test_get_query_string_parameter_wrong_type(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidParamTypeError):
        validator.get_query_string_parameter("invalid_type_param", expected_type=int)
    expected_message = ValidationMessages.Error.INVALID_TYPE.format(
        parameter="invalid_type_param",
        actual="str",
        expected="int",
    )
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", [EVENT_NAMES["VALID"]], indirect=True)
def test_get_query_string_parameter_not_in_allowed_values(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidParamValueError):
        validator.get_query_string_parameter(
            "valid_param",
            allowed_values=["other_value"],
        )
    expected_message = ValidationMessages.Error.PARAMETER_NOT_ALLOWED.format(
        parameter="valid_param",
        value="value",
        allowed_values="['other_value']",
    )
    mock_logger.error.assert_called_once_with(expected_message)


# ====== TESTS: Path Parameter ====================================================
@pytest.mark.parametrize("event", [EVENT_NAMES["MISSING_PATH"]], indirect=True)
def test_get_path_parameter_missing(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(MissingParameterError):
        validator.get_path_parameter("missing_param")
    expected_message = ValidationMessages.Error.MISSING_PARAMETER.format(parameter="missing_param")
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", [EVENT_NAMES["VALID"]], indirect=True)
def test_get_path_parameter_exists(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    assert validator.get_path_parameter("valid_param") == "value"


@pytest.mark.parametrize("event", [EVENT_NAMES["INVALID_PATH_TYPE"]], indirect=True)
def test_get_path_parameter_wrong_type(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidParamTypeError):
        validator.get_path_parameter("invalid_type_param", expected_type=str)
    expected_message = ValidationMessages.Error.INVALID_TYPE.format(
        parameter="invalid_type_param",
        actual="int",
        expected="str",
    )
    mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.parametrize("event", [EVENT_NAMES["VALID"]], indirect=True)
def test_get_path_parameter_not_in_allowed_values(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(InvalidParamValueError):
        validator.get_path_parameter(
            "valid_param",
            allowed_values=["other_value"],
        )
    expected_message = ValidationMessages.Error.PARAMETER_NOT_ALLOWED.format(
        parameter="valid_param",
        value="value",
        allowed_values="['other_value']",
    )
    mock_logger.error.assert_called_once_with(expected_message)


# ====== TESTS: Authorizer Parameter ==============================================
@pytest.mark.parametrize("event", [EVENT_NAMES["MISSING_AUTHORIZER"]], indirect=True)
def test_get_authorizer_parameter_missing(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    with pytest.raises(MissingAuthorizerError):
        validator.get_authorizer_parameter("missing_param")
    expected_message = ValidationMessages.Error.UNAUTHORIZED
    mock_logger.error.assert_any_call(expected_message)


@pytest.mark.parametrize("event", [EVENT_NAMES["VALID"]], indirect=True)
def test_get_authorizer_parameter_exists(validator_with_mocked_logger):
    validator, mock_logger = validator_with_mocked_logger
    assert validator.get_authorizer_parameter("valid_param") == "value"
    mock_logger.info.assert_any_call(
        ValidationMessages.Info.AUTHORIZE_SUCCESSFUL.format(parameter="valid_param")
    )
