from unittest.mock import patch

import pytest
from botocore.exceptions import BotoCoreError, ClientError

from aws.api.v1.src.shared.services.aws.lambdas.lambda_invocation_service import (
    LambdaInvoker,
    MediaProcessingError,
)


# Mock boto3 client
@pytest.fixture
def mock_lambda_client():
    with patch("boto3.client") as mock_client:
        yield mock_client.return_value


class TestLambdaInvoker:
    def test_invoke_success(self, mock_lambda_client):
        mock_lambda_client.invoke.return_value = {"StatusCode": 200, "SomeOtherField": "SomeValue"}

        invoker = LambdaInvoker()
        response = invoker.invoke("fake_arn", {"key": "value"})

        assert response["StatusCode"] == 200
        assert response["SomeOtherField"] == "SomeValue"

    def test_invoke_boto_core_error(self, mock_lambda_client):
        mock_lambda_client.invoke.side_effect = BotoCoreError()

        invoker = LambdaInvoker()

        with pytest.raises(
            MediaProcessingError,
            match="An error occurred during preprocessing",
        ):
            invoker.invoke("fake_arn", {"key": "value"})

    def test_invoke_client_error(self, mock_lambda_client):
        error_msg = ClientError({}, "some_operation")
        mock_lambda_client.invoke.side_effect = error_msg

        invoker = LambdaInvoker()

        with pytest.raises(
            MediaProcessingError,
            match="An error occurred during preprocessing",
        ):
            invoker.invoke("fake_arn", {"key": "value"})

    def test_process_response_forbidden(self, mock_lambda_client):
        response = {"StatusCode": 403}

        invoker = LambdaInvoker()

        with pytest.raises(MediaProcessingError, match="An error occurred during preprocessing"):
            invoker._process_response(response)

    def test_process_response_not_found(self, mock_lambda_client):
        response = {"StatusCode": 404}

        invoker = LambdaInvoker()

        with pytest.raises(MediaProcessingError, match="An error occurred during preprocessing"):
            invoker._process_response(response)

    def test_process_response_unexpected_status_code(self, mock_lambda_client):
        response = {"StatusCode": 500}

        invoker = LambdaInvoker()

        with pytest.raises(MediaProcessingError, match="An error occurred during preprocessing"):
            invoker._process_response(response)
