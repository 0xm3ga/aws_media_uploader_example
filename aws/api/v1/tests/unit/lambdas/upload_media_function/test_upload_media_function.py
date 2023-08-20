import json
from http import HTTPStatus

import pytest

from aws.api.v1.src.lambdas.upload_media_function.app import lambda_handler
from shared.services.error_handler import AppError


@pytest.fixture
def mock_dependencies(mocker):
    module_path = "aws.api.v1.src.lambdas.upload_media_function.app"

    # Mock the dependencies and return their mocked instances
    mock_env = mocker.patch(f"{module_path}.Environment")
    mock_validator = mocker.patch(f"{module_path}.EventValidator")
    mock_media_factory = mocker.patch(f"{module_path}.MediaFactory")
    mock_s3_presign = mocker.patch(f"{module_path}.S3PresignService")
    mock_api_base = mocker.patch(f"{module_path}.ApiBaseService")

    return {
        "env": mock_env.return_value,
        "validator": mock_validator.return_value,
        "media": mock_media_factory.return_value.create_media_from_content_type.return_value,
        "s3_presign": mock_s3_presign.return_value,
        "api_base": mock_api_base,
    }


@pytest.fixture
def event_and_context():
    event = {
        "headers": {"Authorization": "Bearer token"},
        "queryStringParameters": {"content_type": "image/jpeg"},
    }
    context = {"aws_request_id": "12345"}
    return event, context


def test_lambda_handler_success(mock_dependencies, event_and_context):
    event, context = event_and_context

    # Mocking the expected behavior of dependencies
    mock_dependencies["env"].fetch_variable.return_value = "raw-media-bucket"
    mock_dependencies["validator"].get_authorizer_parameter.return_value = "username"
    mock_dependencies["validator"].get_query_string_parameter.return_value = "image/jpeg"
    mock_dependencies["s3_presign"].generate_presigned_url.return_value = (
        "filename",
        "presigned-url",
    )

    expected_response = {
        "statusCode": HTTPStatus.OK,
        "body": {"uploadURL": "presigned-url", "filename": "filename"},
    }
    mock_dependencies["api_base"].create_response.return_value = expected_response

    # Call the lambda handler and assert
    actual_response = lambda_handler(event, context)
    assert actual_response == expected_response


@pytest.mark.parametrize(
    "error, expected_response",
    [
        (
            AppError("Invalid content type.", "Invalid content type.", HTTPStatus.BAD_REQUEST),
            {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "body": json.dumps({"message": "Invalid content type."}),
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
    mock_dependencies["validator"].get_query_string_parameter.side_effect = error

    # Call the lambda handler and assert
    actual_response = lambda_handler(event, context)
    assert actual_response == expected_response
