import json
import re
from unittest.mock import MagicMock

import pytest

from aws.api.v1.src.shared.services.aws.lambdas.image_processing_service import (
    Extension,
    ImageProcessingInvoker,
    LambdaInvoker,
    MediaProcessingError,
    Size,
)

# ===================== CONSTANTS =====================
MOCK_BUCKET = "test_bucket"
MOCK_KEY = "test_key"
MOCK_FILENAME = "test_file"
MOCK_EXTENSION = Extension.JPEG
MOCK_SIZES = [Size.SMALL]

# Sample mock response payload
MOCK_RESPONSE_PAYLOAD = {
    "Payload": MagicMock(read=MagicMock(return_value=json.dumps({"test_key": "test_value"})))
}


# ===================== FIXTURES =====================
@pytest.fixture
def mocked_lambda_invoker():
    """Fixture to provide a mocked instance of LambdaInvoker for tests."""
    invoker = LambdaInvoker()
    invoker.invoke = MagicMock(return_value=MOCK_RESPONSE_PAYLOAD)
    return invoker


@pytest.fixture
def image_processing_invoker(mocked_lambda_invoker):
    """
    Fixture to provide an ImageProcessingInvoker instance with a mocked LambdaInvoker for tests.
    """
    invoker = ImageProcessingInvoker()
    invoker.lambda_invoker = mocked_lambda_invoker
    return invoker


# ===================== TEST CLASSES =====================
class TestInvokeLambdaFunction:
    def test_invoke_lambda_function(self, image_processing_invoker):
        """Test invoking the lambda function with expected payload."""
        response = image_processing_invoker.invoke_lambda_function(
            MOCK_BUCKET, MOCK_KEY, MOCK_FILENAME, MOCK_EXTENSION, MOCK_SIZES
        )
        assert response == {"test_key": "test_value"}


class TestCreatePayload:
    def test_create_payload(self, image_processing_invoker):
        """Test creating the expected payload for the lambda function."""
        payload = image_processing_invoker._create_payload(
            MOCK_BUCKET, MOCK_KEY, MOCK_FILENAME, MOCK_EXTENSION, MOCK_SIZES
        )
        expected_payload = {
            "bucket": MOCK_BUCKET,
            "key": MOCK_KEY,
            "filename": MOCK_FILENAME,
            "extension": MOCK_EXTENSION.value,
            "sizes": [size.name for size in MOCK_SIZES],
        }
        assert payload == expected_payload


class TestExtractPayloadFromResponse:
    def test_extract_payload_from_response(self, image_processing_invoker):
        """Test extracting the payload from the lambda response."""
        response_payload = image_processing_invoker._extract_payload_from_response(
            MOCK_RESPONSE_PAYLOAD
        )
        assert response_payload == {"test_key": "test_value"}

    def test_extract_payload_from_response_error(self, image_processing_invoker):
        """Test error handling when payload extraction fails."""
        error_response = {
            "Payload": MagicMock(read=MagicMock(side_effect=json.JSONDecodeError("msg", "doc", 0)))
        }

        expected_error_message = "An error occurred during preprocessing"
        with pytest.raises(MediaProcessingError, match=re.escape(expected_error_message)):
            image_processing_invoker._extract_payload_from_response(error_response)


class TestCheckResponseForErrors:
    def test_check_response_for_errors_no_error(self, image_processing_invoker):
        """Test that no exception is raised when there are no errors in the lambda response."""
        response_payload = {}
        image_processing_invoker._check_response_for_errors(response_payload)

    def test_check_response_for_errors_with_error(self, image_processing_invoker):
        """Test error handling when there's an 'errorMessage' in the lambda response."""
        error_response = {"errorMessage": "Sample error message"}

        expected_error_message = "An error occurred during preprocessing"
        with pytest.raises(
            MediaProcessingError,
            match=re.escape(expected_error_message),
        ):
            image_processing_invoker._check_response_for_errors(error_response)
