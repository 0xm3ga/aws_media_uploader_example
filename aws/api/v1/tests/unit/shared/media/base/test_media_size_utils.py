import pytest

from aws.api.v1.src.shared.media.base import (
    AspectRatio,
    InvalidAspectRatioError,
    InvalidMediaTypeError,
    InvalidSizeError,
    MediaSizeUtils,
    MediaType,
    Size,
)

# ===================== TESTS: allowed_sizes =====================


def test_allowed_sizes():
    """Test retrieving all allowed sizes."""
    sizes = MediaSizeUtils.allowed_sizes()
    assert sizes == {size.value for size in Size}


# ===================== TESTS: allowed_aspect_ratios =====================


def test_allowed_aspect_ratios():
    """Test retrieving all allowed aspect ratios."""
    ratios = MediaSizeUtils.allowed_aspect_ratios()
    assert ratios == {ratio.value for ratio in AspectRatio}


# ===================== TESTS: is_size_allowed =====================

VALID_SIZES = [size.value for size in Size]
INVALID_SIZES = ["InvalidSize1", "InvalidSize2"]


@pytest.mark.parametrize("size", VALID_SIZES)
def test_is_size_allowed_valid(size):
    """Test valid sizes."""
    assert MediaSizeUtils.is_size_allowed(size)


@pytest.mark.parametrize("size", INVALID_SIZES)
def test_is_size_allowed_invalid(size):
    """Test invalid sizes."""
    with pytest.raises(InvalidSizeError):
        MediaSizeUtils.is_size_allowed(size)


# ===================== TESTS: is_aspect_ratio_allowed =====================

VALID_ASPECT_RATIOS = [ratio.value for ratio in AspectRatio]
INVALID_ASPECT_RATIOS = ["InvalidRatio1", "InvalidRatio2"]


@pytest.mark.parametrize("ratio", VALID_ASPECT_RATIOS)
def test_is_aspect_ratio_allowed_valid(ratio):
    """Test valid aspect ratios."""
    assert MediaSizeUtils.is_aspect_ratio_allowed(ratio)


@pytest.mark.parametrize("ratio", INVALID_ASPECT_RATIOS)
def test_is_aspect_ratio_allowed_invalid(ratio):
    """Test invalid aspect ratios."""
    with pytest.raises(InvalidAspectRatioError):
        MediaSizeUtils.is_aspect_ratio_allowed(ratio)


# ===================== TESTS: allowed_dimensions =====================

VALID_MEDIA_TYPES = [MediaType.IMAGE, MediaType.VIDEO]
INVALID_MEDIA_TYPES = ["InvalidMediaType1", "InvalidMediaType2"]


@pytest.mark.parametrize("media_type", VALID_MEDIA_TYPES)
def test_allowed_dimensions_valid_media_type(media_type):
    MediaSizeUtils.allowed_dimensions(media_type)


@pytest.mark.parametrize("media_type", INVALID_MEDIA_TYPES)
def test_allowed_dimensions_invalid_media_type(media_type):
    """Test retrieving dimensions with invalid media type."""
    with pytest.raises(InvalidMediaTypeError):
        MediaSizeUtils.allowed_dimensions(media_type)


# ===================== TESTS: get_dimensions =====================
VALID_MEDIA_TYPE = MediaType.IMAGE  # Or some valid media type
VALID_ASPECT_RATIO = AspectRatio.AR_1_BY_1  # Replace with actual aspect ratio
VALID_SIZE = Size.HUGE  # Replace with actual size


def test_get_dimensions_valid():
    """Test retrieving dimensions with valid inputs."""
    dimensions = MediaSizeUtils.get_dimensions(VALID_MEDIA_TYPE, VALID_ASPECT_RATIO, VALID_SIZE)
    # Asserting the type, you can add more checks based on expected values.
    assert isinstance(dimensions, tuple) and len(dimensions) == 2
