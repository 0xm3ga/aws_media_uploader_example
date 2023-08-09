from unittest.mock import Mock, PropertyMock, patch

import pytest

from aws.api.v1.src.shared.services.aws.s3.s3_presigned_service import (
    ImageMedia,
    S3PresignService,
    VideoMedia,
)

# ===================== CONSTANTS =====================
VALID_USERNAME = "test_user"
VALID_RAW_BUCKET_NAME = "test-raw-bucket"
IMAGE_S3_PREFIX = "image_prefix"
VIDEO_S3_PREFIX = "video_prefix"
IMAGE_CONTENT_TYPE = "image/jpeg"
VIDEO_CONTENT_TYPE = "video/mp4"

mock_image_media = Mock(spec=ImageMedia)
type(mock_image_media).s3_prefix = PropertyMock(return_value=IMAGE_S3_PREFIX)
type(mock_image_media).content_type = PropertyMock(return_value=IMAGE_CONTENT_TYPE)

mock_video_media = Mock(spec=VideoMedia)
type(mock_video_media).s3_prefix = PropertyMock(return_value=VIDEO_S3_PREFIX)
type(mock_video_media).content_type = PropertyMock(return_value=VIDEO_CONTENT_TYPE)

# ===================== TESTS: S3PresignService =====================


@patch(
    "aws.api.v1.src.shared.services.aws.s3.s3_presigned_service.uuid.uuid4",
    return_value="mock-uuid",
)
@patch("boto3.client")
def test_generate_presigned_url_for_image(mock_boto3_client, mock_uuid):
    """Test generating a presigned S3 URL for an image."""
    mock_client = Mock()
    mock_client.generate_presigned_url.return_value = "mock-presigned-url"
    mock_boto3_client.return_value = mock_client

    s3_presign_service = S3PresignService()
    filename, presigned_url = s3_presign_service.generate_presigned_url(
        mock_image_media, VALID_USERNAME, VALID_RAW_BUCKET_NAME
    )

    assert filename == "mock-uuid"
    assert presigned_url == "mock-presigned-url"


@patch(
    "aws.api.v1.src.shared.services.aws.s3.s3_presigned_service.uuid.uuid4",
    return_value="mock-uuid",
)
@patch("boto3.client")
def test_generate_presigned_url_for_video(mock_boto3_client, mock_uuid):
    """Test generating a presigned S3 URL for a video."""
    mock_client = Mock()
    mock_client.generate_presigned_url.return_value = "mock-presigned-url"
    mock_boto3_client.return_value = mock_client

    s3_presign_service = S3PresignService()
    filename, presigned_url = s3_presign_service.generate_presigned_url(
        mock_video_media, VALID_USERNAME, VALID_RAW_BUCKET_NAME
    )

    assert filename == "mock-uuid"
    assert presigned_url == "mock-presigned-url"


@patch("boto3.client")
def test_generate_presigned_url_error(mock_boto3_client):
    """Test error scenario when generating a presigned S3 URL."""
    mock_client = Mock()
    mock_client.generate_presigned_url.side_effect = Exception("Mock exception")
    mock_boto3_client.return_value = mock_client

    s3_presign_service = S3PresignService()

    with pytest.raises(Exception, match="Mock exception"):
        s3_presign_service.generate_presigned_url(
            mock_image_media, VALID_USERNAME, VALID_RAW_BUCKET_NAME
        )
