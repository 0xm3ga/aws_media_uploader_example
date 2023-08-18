import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.models.media_request import (
    MediaRequest,
    ObjectNotFoundError,
)

# Constants used in tests
FILENAME = "test_file"
SIZE_STR = "SMALL"
EXTENSION_STR = "jpg"
MEDIA_INFO = ("username", "image/jpeg")
MEDIA_URL = "https://test.com/test_file_SMALL.jpg"


@pytest.fixture
def mock_media_request(mocker):
    module_path = "aws.api.v1.src.lambdas.retrieve_media_function.models.media_request"

    mocker.patch(f"{module_path}.S3BaseService", autospec=True)
    mocker.patch(f"{module_path}.RdsBaseService", autospec=True)
    media_request = MediaRequest("processed_bucket", "raw_bucket", "test.com")
    yield media_request


def setup_mocks(mock_media_request, mocker, exists=False):
    mocker.patch.object(
        mock_media_request,
        "_check_object_exists",
        side_effect=[exists, True],
    )
    mocker.patch.object(
        mock_media_request.rds_service,
        "fetch_media_info_from_rds",
        return_value=MEDIA_INFO,
    )
    mocker.patch.object(
        mock_media_request.s3_service,
        "construct_media_url",
        return_value=MEDIA_URL,
    )


class TestMediaRequest:
    def test_process_existing_processed_key_returns_url(self, mock_media_request, mocker):
        """
        Test that the process method returns the correct URL when the processed key exists.
        """

        setup_mocks(mock_media_request, mocker, exists=True)
        mock_create_processor = mocker.patch.object(mock_media_request, "_create_processor")
        mocker.patch.object(mock_create_processor, "process", return_value=MEDIA_URL)

        result = mock_media_request.process(FILENAME, SIZE_STR, EXTENSION_STR)

        assert result == MEDIA_URL

    def test_process_non_existing_processed_key_calls_create_processor(
        self, mock_media_request, mocker
    ):
        """
        Test that the process method correctly invokes the create_processor method when the
        processed key doesn't exist.
        """
        setup_mocks(mock_media_request, mocker, exists=False)

        result = mock_media_request.process(FILENAME, SIZE_STR, EXTENSION_STR)

        assert result == MEDIA_URL


class TestObjectCheck:
    def test_check_object_exists_returns_false(self, mock_media_request, mocker):
        mocker.patch.object(mock_media_request.s3_service, "object_exists", return_value=False)
        result = mock_media_request._check_object_exists("bucket", "key")
        assert not result

    def test_check_object_exists_required_raises_exception(self, mock_media_request, mocker):
        mocker.patch.object(mock_media_request.s3_service, "object_exists", return_value=False)
        with pytest.raises(ObjectNotFoundError):
            mock_media_request._check_object_exists("bucket", "key", required=True)
