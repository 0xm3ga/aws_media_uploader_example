import json
from http import HTTPStatus

import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.app import lambda_handler
from aws.api.v1.src.shared.services.error_handler import AppError


@pytest.fixture
def mock_dependencies(mocker):
    module_path = "aws.api.v1.src.lambdas.retrieve_media_function.app"

    # Mock the dependencies and return their mocked instances
    mock_env = mocker.patch(f"{module_path}.Environment")
    mock_validator = mocker.patch(f"{module_path}.EventValidator")
    mock_media_request = mocker.patch(f"{module_path}.MediaRequest")
    mock_api_base = mocker.patch(f"{module_path}.ApiBaseService")

    return {
        "env": mock_env.return_value,
        "validator": mock_validator.return_value,
        "media_request": mock_media_request.return_value,
        "api_base": mock_api_base,
    }


@pytest.fixture
def event_and_context():
    event = {
        "pathParameters": {"filename": "sample.jpg"},
        "queryStringParameters": {"size": "medium", "extension": "jpg"},
    }
    context = {"aws_request_id": "12345"}
    return event, context


def test_lambda_handler_success(mock_dependencies, event_and_context):
    event, context = event_and_context

    # Mocking the expected behavior of dependencies
    mock_dependencies["env"].fetch_variable.return_value = "raw-media-bucket"
    mock_dependencies["validator"].get_path_parameter.return_value = "sample.jpg"
    mock_dependencies["validator"].get_query_string_parameter.side_effect = ["medium", "jpg"]
    mock_dependencies["media_request"].process.return_value = "https://media-url"

    expected_response = {
        "statusCode": HTTPStatus.FOUND,
        "headers": {"Location": "https://media-url"},
    }
    mock_dependencies["api_base"].create_redirect.return_value = expected_response

    # Call the lambda handler and assert
    actual_response = lambda_handler(event, context)
    assert actual_response == expected_response


@pytest.mark.parametrize(
    "error, expected_response",
    [
        (
            AppError("Invalid filename.", "Invalid filename.", HTTPStatus.BAD_REQUEST),
            {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "body": json.dumps({"message": "Invalid filename."}),
            },
        ),
        (
            Exception("Some unexpected error"),
            {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": json.dumps({"message": "Internal server error."}),
            },
        ),
    ],
)
def test_lambda_handler_errors(mock_dependencies, event_and_context, error, expected_response):
    event, context = event_and_context

    # Mocking the expected behavior of dependencies
    mock_dependencies["validator"].get_path_parameter.side_effect = error

    # Call the lambda handler and assert
    actual_response = lambda_handler(event, context)
    assert actual_response == expected_response
