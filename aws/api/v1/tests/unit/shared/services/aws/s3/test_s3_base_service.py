from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError

from shared.services.aws.s3.s3_base_service import S3BaseService

# ===================== CONSTANTS =====================

VALID_BUCKET = "test-bucket"
VALID_KEY = "test-key"
VALID_FILENAME = "testfile"
VALID_SIZE = "small"
VALID_EXTENSION = "jpg"
VALID_USERNAME = "user1"
VALID_S3_PREFIX = "prefix"
VALID_DOMAIN = "example.com"
VALID_PATH = "media/test.jpg"

INVALID_TYPE = 123  # Not a string
EMPTY_STRING = ""  # Empty string

CLIENT_ERROR_NOT_FOUND_RESPONSE = {"Error": {"Code": HTTPStatus.NOT_FOUND}}

CLIENT_ERROR_OTHER_RESPONSE = {"Error": {"Code": HTTPStatus.BAD_REQUEST}}

# ===================== TESTS: S3BaseService =====================


@patch("boto3.client")
def test_object_exists_true(mock_boto3_client):
    """Test object exists returns true."""
    mock_boto3_client.return_value.head_object.return_value = {}
    s3_service = S3BaseService()
    assert s3_service.object_exists(VALID_BUCKET, VALID_KEY)


@patch("boto3.client")
def test_object_exists_false(mock_boto3_client):
    """Test object exists returns false."""
    mock_instance = Mock()
    mock_instance.head_object.side_effect = ClientError(
        CLIENT_ERROR_NOT_FOUND_RESPONSE, "head_object"
    )
    mock_boto3_client.return_value = mock_instance
    s3_service = S3BaseService()
    assert not s3_service.object_exists(VALID_BUCKET, VALID_KEY)


@patch("boto3.client")
def test_object_exists_error(mock_boto3_client):
    """Test object exists raises unexpected error."""
    mock_instance = Mock()
    mock_instance.head_object.side_effect = ClientError(CLIENT_ERROR_OTHER_RESPONSE, "head_object")
    mock_boto3_client.return_value = mock_instance
    s3_service = S3BaseService()
    with pytest.raises(ClientError):
        s3_service.object_exists(VALID_BUCKET, VALID_KEY)


def test_construct_processed_media_key():
    """Test key generation for processed media."""
    s3_service = S3BaseService()
    key = s3_service.construct_processed_media_key(VALID_FILENAME, VALID_SIZE, VALID_EXTENSION)
    assert key == f"{VALID_FILENAME}/{VALID_SIZE}.{VALID_EXTENSION}"


def test_construct_raw_media_key():
    """Test key generation for raw media file."""
    s3_service = S3BaseService()
    key = s3_service.construct_raw_media_key(VALID_FILENAME, VALID_USERNAME, VALID_S3_PREFIX)
    assert key == f"{VALID_USERNAME}/{VALID_S3_PREFIX}/{VALID_FILENAME}"


def test_construct_media_url():
    """Test media URL generation."""
    s3_service = S3BaseService()
    url = s3_service.construct_media_url(VALID_DOMAIN, VALID_PATH)
    assert url == f"https://{VALID_DOMAIN}/{VALID_PATH}"


@pytest.mark.parametrize(
    "filename, size, extension, exception",
    [
        (EMPTY_STRING, VALID_SIZE, VALID_EXTENSION, ValueError),
        (VALID_FILENAME, INVALID_TYPE, VALID_EXTENSION, TypeError),
        (VALID_FILENAME, VALID_SIZE, INVALID_TYPE, TypeError),
    ],
)
def test_construct_processed_media_key_errors(filename, size, extension, exception):
    """Test error scenarios for construct_processed_media_key."""
    s3_service = S3BaseService()
    with pytest.raises(exception):
        s3_service.construct_processed_media_key(filename, size, extension)


@pytest.mark.parametrize(
    "filename, username, s3_prefix, exception",
    [
        (EMPTY_STRING, VALID_USERNAME, VALID_S3_PREFIX, ValueError),
        (VALID_FILENAME, INVALID_TYPE, VALID_S3_PREFIX, TypeError),
        (VALID_FILENAME, VALID_USERNAME, INVALID_TYPE, TypeError),
    ],
)
def test_construct_raw_media_key_errors(filename, username, s3_prefix, exception):
    """Test error scenarios for construct_raw_media_key."""
    s3_service = S3BaseService()
    with pytest.raises(exception):
        s3_service.construct_raw_media_key(filename, username, s3_prefix)


@pytest.mark.parametrize(
    "domain_name, path, exception",
    [
        (INVALID_TYPE, VALID_PATH, ValueError),
        (VALID_DOMAIN, INVALID_TYPE, ValueError),
    ],
)
def test_construct_media_url_errors(domain_name, path, exception):
    """Test error scenarios for construct_media_url."""
    s3_service = S3BaseService()
    with pytest.raises(exception):
        s3_service.construct_media_url(domain_name, path)
