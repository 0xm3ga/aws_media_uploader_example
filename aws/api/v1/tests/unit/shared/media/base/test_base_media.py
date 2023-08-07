import pytest

from aws.api.v1.src.shared.media.base import BaseMedia, MediaType

# ===================== CONSTANTS =====================
S3_PREFIX_TEST_INPUTS = [
    (MediaType.IMAGE, "images"),
    (MediaType.VIDEO, "videos"),
]


# ===================== TESTS: BaseMedia =====================
def test_base_media_initialization():
    """Test that the BaseMedia class is initialized with the correct media type."""
    media = BaseMedia(MediaType.IMAGE)
    assert media._media_type == MediaType.IMAGE


@pytest.mark.parametrize("media_type, expected_prefix", S3_PREFIX_TEST_INPUTS)
def test_base_media_s3_prefix(media_type, expected_prefix):
    """Test that the s3_prefix property returns the correct prefix based on the media type."""
    media = BaseMedia(media_type)
    assert media.s3_prefix == expected_prefix
