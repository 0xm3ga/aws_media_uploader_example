from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.app import lambda_handler


@pytest.fixture
def mock_event():
    return {
        "pathParameters": {"filename": "testfile.jpg"},
        "queryStringParameters": {"extension": "jpeg", "size": "large"},
    }


@pytest.fixture
def mock_context():
    context = Mock()
    context.aws_request_id = "mock_request_id"
    context.log_group_name = "mock_log_group"
    context.log_stream_name = "mock_log_stream"
    return context


@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.Environment")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.MediaRequest")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.extract_and_validate_event")
def test_lambda_handler_success(
    mock_extract, mock_media_request, mock_env, mock_event, mock_context
):
    mock_extract.return_value = ("filename", "size", "extension")
    mock_media_request_instance = mock_media_request.return_value
    mock_media_request_instance.process.return_value = "http://test.url"
    mock_env_instance = mock_env.return_value
    mock_env_instance.fetch_variable.side_effect = ["bucket1", "bucket2", "domain"]

    response = lambda_handler(mock_event, mock_context)

    assert response["statusCode"] == HTTPStatus.FOUND


@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.Environment")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.MediaRequest")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.extract_and_validate_event")
@patch("aws.api.v1.src.lambdas.retrieve_media_function.app.logger")
def test_lambda_handler_generic_exception(
    mock_logger,
    mock_extract,
    mock_media_request,
    mock_env,
    mock_event,
    mock_context,
):
    mock_extract.side_effect = Exception("Generic error for testing.")
    mock_env_instance = mock_env.return_value
    mock_env_instance.fetch_variable.side_effect = ["bucket1", "bucket2", "domain"]

    response = lambda_handler(mock_event, mock_context)

    assert response["statusCode"] == HTTPStatus.INTERNAL_SERVER_ERROR
