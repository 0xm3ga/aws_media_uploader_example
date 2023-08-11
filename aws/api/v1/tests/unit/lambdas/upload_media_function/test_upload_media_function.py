import json
from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from aws.api.v1.src.lambdas.upload_media_function.app import (
    Environment,
    EventValidator,
    HttpErrorMessages,
    InvalidContentTypeError,
    InvalidTypeError,
    InvalidValueError,
    MediaFactory,
    MissingParameterError,
    S3PresignService,
    UnauthorizedError,
    lambda_handler,
    logger,
)


@pytest.fixture
def mock_logger():
    with patch.object(logger, "error", new_callable=Mock) as mock_logger_error, patch.object(
        logger, "info", new_callable=Mock
    ) as mock_logger_info:
        yield mock_logger_error, mock_logger_info


@pytest.fixture
def mock_environment():
    with patch.object(Environment, "fetch_required_variables") as mock_env_all, patch.object(
        Environment, "fetch_variable", return_value="test-bucket"
    ) as mock_env_var:
        yield mock_env_all, mock_env_var


@pytest.fixture
def mock_event_validator():
    with patch.object(
        EventValidator, "get_authorizer_parameter", return_value="test_user"
    ) as mock_auth, patch.object(
        EventValidator, "get_query_string_parameter", return_value="image/jpeg"
    ) as mock_query_string_parameter:
        yield mock_auth, mock_query_string_parameter


@pytest.fixture
def mock_media_factory():
    with patch.object(
        MediaFactory, "create_media_from_content_type", return_value="media"
    ) as mock_method:
        yield mock_method


@pytest.fixture
def mock_s3_presign_service():
    with patch.object(
        S3PresignService, "generate_presigned_url", return_value=("filename", "presigned_url")
    ) as mock_method:
        yield mock_method


def test_lambda_handler_happy_path(
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
):
    event = {}
    result = lambda_handler(event, None)
    assert result["statusCode"] == HTTPStatus.OK


def test_lambda_handler_environment_fetch_var_exceptions(
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
    mock_logger,
):
    error_message = "Missing required [env_var_1, env_var_2]"

    mock_error_info, _ = mock_logger
    _, mock_env_var = mock_environment
    mock_env_var.side_effect = Exception(error_message)

    event = {}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert body == HttpErrorMessages.INTERNAL_SERVER_ERROR
    mock_error_info.assert_called_with(
        HttpErrorMessages.UNEXPECTED_ERROR.format(error=str(error_message))
    )


def test_lambda_handler_environment_all_vars_exceptions(
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
    mock_logger,
):
    error_message = "Missing env var"

    mock_error_info, _ = mock_logger
    mock_env_all, _ = mock_environment
    mock_env_all.side_effect = Exception(error_message)

    event = {}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert body == HttpErrorMessages.INTERNAL_SERVER_ERROR
    mock_error_info.assert_called_with(
        HttpErrorMessages.UNEXPECTED_ERROR.format(error=str(error_message))
    )


def test_lambda_handler_event_validator_auth_exception(
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
    mock_logger,
):
    mock_error_info, _ = mock_logger
    mock_auth, _ = mock_event_validator
    mock_auth.side_effect = UnauthorizedError

    event = {}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert body == HttpErrorMessages.UNAUTHORIZED
    mock_error_info.assert_called_with(HttpErrorMessages.UNAUTHORIZED)


@pytest.mark.parametrize(
    "exception, error_message",
    [
        (
            MissingParameterError(parameter="content_type"),
            MissingParameterError(parameter="content_type").message,
        ),
        (
            InvalidTypeError(parameter="content_type", actual=int, expected=str),
            InvalidTypeError(parameter="content_type", actual=int, expected=str).message,
        ),
        (
            InvalidValueError(parameter="content_type", value="invalid_value", allowed_values=None),
            InvalidValueError(
                parameter="content_type", value="invalid_value", allowed_values=None
            ).message,
        ),
    ],
)
def test_lambda_handler_event_validator_query_string_parameter_exception(
    exception,
    error_message,
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
    mock_logger,
):
    mock_error_info, _ = mock_logger
    _, mock_query_string_parameter = mock_event_validator
    mock_query_string_parameter.side_effect = exception

    event = {}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.BAD_REQUEST
    assert body == error_message
    mock_error_info.assert_called_with(
        HttpErrorMessages.UNEXPECTED_ERROR.format(error=error_message)
    )


@pytest.mark.parametrize(
    "exception, error_message",
    [
        (
            InvalidContentTypeError(content_type="image/mp4"),
            InvalidContentTypeError(content_type="image/mp4").message,
        ),
    ],
)
def test_lambda_handler_media_factory(
    exception,
    error_message,
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
    mock_logger,
):
    mock_error_info, _ = mock_logger
    mock_media_factory.side_effect = exception

    event = {}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.BAD_REQUEST
    assert body == error_message
    mock_error_info.assert_called_with(
        HttpErrorMessages.UNEXPECTED_ERROR.format(error=error_message)
    )


def test_lambda_handler_s3_presign_service(
    mock_environment,
    mock_event_validator,
    mock_media_factory,
    mock_s3_presign_service,
    mock_logger,
):
    expected_presigned_url = "https://example.com/presigned-url"
    expected_filename = "test_filename"

    mock_s3_presign_service.return_value = (expected_filename, expected_presigned_url)

    event = {}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == HTTPStatus.OK
    assert body["uploadURL"] == expected_presigned_url
    assert body["filename"] == expected_filename
