import json
from http import HTTPStatus
from unittest.mock import patch

import pytest

from aws.api.v1.src.shared.services.aws.api.api_base_service import ApiBaseService, ApiMessages

# ===================== CONSTANTS =====================
VALID_MESSAGE_OBJECT = {"message": "Hello, World!"}
INVALID_MESSAGE_OBJECT = {"object": set([1, 2, 3])}
VALID_STATUS_CODE = HTTPStatus.OK
VALID_REDIRECT_LOCATION = "/new/path"
INVALID_REDIRECT_LOCATION = 12345  # Not a string

# ===================== TESTS: ApiBaseService =====================


class TestApiBaseService:
    @pytest.mark.parametrize(
        "message, expected_body",
        [
            (VALID_MESSAGE_OBJECT, json.dumps(VALID_MESSAGE_OBJECT)),
            (INVALID_MESSAGE_OBJECT, ValueError),
        ],
    )
    def test_create_response_varied_messages(self, message, expected_body):
        """Test creating responses with varied message types."""
        if expected_body == ValueError:
            with pytest.raises(ValueError):
                ApiBaseService.create_response(VALID_STATUS_CODE, message)
        else:
            response = ApiBaseService.create_response(VALID_STATUS_CODE, message)
            assert response["statusCode"] == VALID_STATUS_CODE.value
            assert response["body"] == expected_body

    @patch("aws.api.v1.src.shared.services.aws.api.api_base_service.logger.info")
    def test_create_response_logging(self, mock_logger_info):
        """Test that creating a response logs the correct information."""
        ApiBaseService.create_response(VALID_STATUS_CODE, VALID_MESSAGE_OBJECT)
        expected_log_message = ApiMessages.Info.RESPONSE_CREATED.format(
            status=VALID_STATUS_CODE, message=json.dumps(VALID_MESSAGE_OBJECT)
        )
        mock_logger_info.assert_called_with(expected_log_message)

    @pytest.mark.parametrize(
        "location, expected_location",
        [
            (VALID_REDIRECT_LOCATION, VALID_REDIRECT_LOCATION),
            (INVALID_REDIRECT_LOCATION, str(INVALID_REDIRECT_LOCATION)),
        ],
    )
    def test_create_redirect_varied_locations(self, location, expected_location):
        """Test creating redirects with varied location types."""
        response = ApiBaseService.create_redirect(VALID_STATUS_CODE, location)
        assert response["statusCode"] == VALID_STATUS_CODE.value
        assert response["headers"]["Location"] == expected_location

    @patch("aws.api.v1.src.shared.services.aws.api.api_base_service.logger.info")
    def test_create_redirect_logging(self, mock_logger_info):
        """Test that creating a redirect logs the correct information."""
        ApiBaseService.create_redirect(VALID_STATUS_CODE, VALID_REDIRECT_LOCATION)
        expected_log_message = ApiMessages.Info.REDIRECT_CREATED.format(
            status=VALID_STATUS_CODE, location=VALID_REDIRECT_LOCATION
        )
        mock_logger_info.assert_called_with(expected_log_message)
