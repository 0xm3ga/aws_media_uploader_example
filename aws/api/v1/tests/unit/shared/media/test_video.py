import pytest

# Local imports
from aws.api.v1.src.shared.media import MediaType, VideoFormat, VideoMedia, VideoSize

# Constants
MP4_CONTENT_TYPE = "video/mp4"
UNKNOWN_SIZE = "extralarge"
UNKNOWN_EXTENSION = "mkv"

# ------------------ Fixtures ------------------


# Parameterized fixture for video formats
@pytest.fixture(params=VideoFormat)
def video_format(request):
    return request.param


# Parameterized fixture for video sizes
@pytest.fixture(params=VideoSize)
def video_size(request):
    return request.param


# ------------------ Tests for VideoFormat ------------------


def test_video_format_media_type(video_format):
    assert video_format.media_type == MediaType.VIDEO.value


def test_video_format_extension_resolution(video_format):
    # If a format has an alias (e.g., jpg -> jpeg), this tests that resolution works
    expected_extension = video_format.value[1]
    assert video_format.extension == expected_extension


def test_video_format_content_type(video_format):
    expected_content_type = f"{MediaType.VIDEO.value}/{video_format.value[1]}"
    assert video_format.content_type == expected_content_type


# ------------------ Tests for VideoSize ------------------


def test_video_size_properties(video_size):
    assert isinstance(video_size.value, tuple)
    assert len(video_size.value) == 2


def test_video_size_is_allowed(video_size):
    assert VideoSize.is_size_allowed(video_size.name.lower())


def test_video_size_is_not_allowed_for_unknown_sizes():
    assert not VideoSize.is_size_allowed(UNKNOWN_SIZE)


# ------------------ Tests for VideoMedia ------------------


def test_video_media_initialization_properties():
    video_media = VideoMedia(content_type=MP4_CONTENT_TYPE)

    assert video_media.media_type == MediaType.VIDEO
    assert video_media.content_type == MP4_CONTENT_TYPE
    assert video_media.s3_prefix == "videos"


# ------------------ Tests for VideoFormat validation ------------------


def test_video_format_is_extension_allowed_for_known_formats(video_format):
    assert VideoFormat.is_extension_allowed(video_format.value[1])


def test_video_format_is_extension_not_allowed_for_unknown_formats():
    assert not VideoFormat.is_extension_allowed(UNKNOWN_EXTENSION)
