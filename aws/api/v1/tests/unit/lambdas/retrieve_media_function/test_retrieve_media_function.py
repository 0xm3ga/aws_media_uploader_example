from http import HTTPStatus
from unittest.mock import patch

import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.app import (
    FileProcessingError,
    InvalidTypeError,
    InvalidValueError,
    MissingParameterError,
    NoCredentialsError,
    ObjectNotFoundError,
    PreprocessingError,
    lambda_handler,
)


@pytest.fixture
def mock_event():
    return {
        "pathParameters": {"filename": "testfile.jpg"},
        "queryStringParameters": {"extension": "jpeg", "size": "large"},
    }


@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.Environment")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.MediaRequest")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.extract_and_validate_event")
def test_lambda_handler_success(mock_extract, mock_media_request, mock_env, mock_event):
    mock_extract.return_value = ("filename", "size", "extension")
    mock_media_request_instance = mock_media_request.return_value
    mock_media_request_instance.process.return_value = "http://test.url"
    mock_env_instance = mock_env.return_value
    mock_env_instance.fetch_variable.side_effect = ["bucket1", "bucket2", "domain"]

    response = lambda_handler(mock_event, None)

    assert response["statusCode"] == HTTPStatus.FOUND


@pytest.mark.parametrize(
    "exception, status, log_message",
    [
        (NoCredentialsError(), HTTPStatus.INTERNAL_SERVER_ERROR, "NO_AWS_CREDENTIALS"),
        (PreprocessingError(), HTTPStatus.BAD_REQUEST, "GENERIC_PROCESSING_ERROR"),
        (
            MissingParameterError(parameter="test"),
            HTTPStatus.BAD_REQUEST,
            "GENERIC_PROCESSING_ERROR",
        ),
        (
            InvalidTypeError(parameter="test", actual=str, expected=int),
            HTTPStatus.BAD_REQUEST,
            "GENERIC_PROCESSING_ERROR",
        ),
        (
            InvalidValueError(
                parameter="param", value="test_value", allowed_values=["allowed_value"]
            ),
            HTTPStatus.BAD_REQUEST,
            "GENERIC_PROCESSING_ERROR",
        ),
        (ObjectNotFoundError(), HTTPStatus.NOT_FOUND, "OBJECT_NOT_FOUND"),
        (FileProcessingError(), HTTPStatus.INTERNAL_SERVER_ERROR, "GENERIC_PROCESSING_ERROR"),
        (Exception(), HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR"),
    ],
)
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.Environment")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.MediaRequest")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.extract_and_validate_event")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.logger")
def test_lambda_handler_exceptions(
    mock_logger,
    mock_extract,
    mock_media_request,
    mock_env,
    exception,
    status,
    log_message,
    mock_event,
):
    mock_extract.side_effect = exception
    mock_env_instance = mock_env.return_value
    mock_env_instance.fetch_variable.side_effect = ["bucket1", "bucket2", "domain"]

    # Configure the mock to return a dictionary when create_response is called
    # mock_api_base.create_response.return_value = {"statusCode": status}

    response = lambda_handler(mock_event, None)

    assert response["statusCode"] == status
