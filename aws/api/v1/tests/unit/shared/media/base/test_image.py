import pytest

from shared.media.base import MediaType, VideoMedia

# ===================== CONSTANTS =====================
VIDEO_MEDIA_CONTENT_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
]


# ===================== TESTS: VideoMedia =====================
@pytest.mark.parametrize("content_type", VIDEO_MEDIA_CONTENT_TYPES)
def test_video_media_content_type_initialization(content_type):
    """Test that the VideoMedia class is initialized with the correct content type."""
    video = VideoMedia(content_type)
    assert video.content_type == content_type


def test_video_media_media_type_initialization():
    """Test that the VideoMedia class is initialized with the correct media type."""
    video = VideoMedia(content_type="video/mp4")
    assert video._media_type == MediaType.VIDEO
