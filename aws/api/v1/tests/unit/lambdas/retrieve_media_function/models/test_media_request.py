from unittest.mock import MagicMock, patch

import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.models.media_request import (
    MediaRequest,
    ObjectNotFoundError,
)


@pytest.fixture
def mock_media_request():
    with patch(
        "aws.api.v1.src.lambdas.retrieve_media_function.models.media_request.S3BaseService"
    ) as mock_s3, patch(
        "aws.api.v1.src.lambdas.retrieve_media_function.models.media_request.RdsBaseService"
    ) as mock_rds:
        media_request = MediaRequest("processed_bucket", "raw_bucket", "test.com")
        media_request.s3_service = mock_s3
        media_request.rds_service = mock_rds

        yield media_request


# def test_process_with_existing_processed_key(mock_media_request):
#     filename = "test_file"
#     size_str = "SMALL"
#     extension_str = "jpg"

#     mock_media_request._check_object_exists = MagicMock(return_value=True)

#     result = mock_media_request.process(filename, size_str, extension_str)

#     assert result == "https://test.com/test_file_SMALL.jpg"


# def test_process_with_non_existing_processed_key(mock_media_request):
#     filename = "test_file"
#     size_str = "SMALL"
#     extension_str = "jpg"

#     mock_media_request._check_object_exists = MagicMock(side_effect=[False, True])
#     mock_media_request.rds_service.fetch_media_info_from_rds = MagicMock(
#         return_value=("username", "image/jpeg")
#     )
#     mock_media_request._create_processor = MagicMock()

#     result = mock_media_request.process(filename, size_str, extension_str)

#     assert result == "https://test.com/test_file_SMALL.jpg"
#     mock_media_request._create_processor.assert_called()


def test_check_object_exists_returns_false(mock_media_request):
    mock_media_request.s3_service.object_exists = MagicMock(return_value=False)

    result = mock_media_request._check_object_exists("bucket", "key")

    assert not result


def test_check_object_exists_required_raises_exception(mock_media_request):
    mock_media_request.s3_service.object_exists = MagicMock(return_value=False)

    with pytest.raises(ObjectNotFoundError):
        mock_media_request._check_object_exists("bucket", "key", required=True)
