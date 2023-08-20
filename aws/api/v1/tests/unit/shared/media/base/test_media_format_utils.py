import pytest

from shared.media.base import (
    Extension,
    InvalidContentTypeError,
    InvalidExtensionError,
    InvalidMediaTypeError,
    MediaFormatUtils,
    MediaType,
)

# ===================== TESTS: allowed_content_types =====================

ALLOWED_CONTENT_TYPES_VALID = [MediaType.VIDEO, MediaType.IMAGE, None]


@pytest.mark.parametrize("media_type", ALLOWED_CONTENT_TYPES_VALID)
def test_allowed_content_types_valid(media_type):
    """Test valid media types for the allowed_content_types method."""
    assert MediaFormatUtils.allowed_content_types(media_type)


ALLOWED_CONTENT_TYPES_INVALID = ["InvalidType1", "InvalidType2"]


@pytest.mark.parametrize("media_type", ALLOWED_CONTENT_TYPES_INVALID)
def test_allowed_content_types_invalid(media_type):
    """Test invalid media types for the allowed_content_types method."""
    with pytest.raises(InvalidMediaTypeError):
        MediaFormatUtils.allowed_content_types(media_type)


# ===================== TESTS: allowed_extensions =====================
ALLOWED_EXTENSIONS_VALID = [MediaType.VIDEO, MediaType.IMAGE, None]


@pytest.mark.parametrize("media_type", ALLOWED_EXTENSIONS_VALID)
def test_allowed_extensions_valid(media_type):
    """Test valid media types for the allowed_extensions method."""
    assert MediaFormatUtils.allowed_extensions(media_type)


ALLOWED_EXTENSIONS_INVALID = ["InvalidType1", "InvalidType2"]


@pytest.mark.parametrize("media_type", ALLOWED_EXTENSIONS_INVALID)
def test_allowed_extensions_invalid(media_type):
    """Test invalid media types for the allowed_extensions method."""
    with pytest.raises(InvalidMediaTypeError):
        MediaFormatUtils.allowed_extensions(media_type)


# ===================== TESTS: is_extension_allowed =====================
IS_EXTENSION_ALLOWED = [
    ("jpeg", MediaType.IMAGE, True),
    ("jpg", MediaType.IMAGE, True),
    ("jpg", None, True),
    ("jpeg", None, True),
    ("mp4", MediaType.VIDEO, True),
    ("mp4", MediaType.IMAGE, False),
    ("mp4", None, True),
    ("mp5", None, False),
    (None, None, False),
    ("", None, False),
    (" ", None, False),
    (".jpeg", None, False),
]


@pytest.mark.parametrize("extension, media_type, expected", IS_EXTENSION_ALLOWED)
def test_is_extension_allowed(extension, media_type, expected):
    """Test the is_extension_allowed method for various scenarios."""
    assert MediaFormatUtils.is_extension_allowed(extension, media_type) == expected


# ===================== TESTS: is_content_type_allowed =====================
IS_CONTENT_TYPE_ALLOWED = [
    ("image/jpeg", MediaType.IMAGE, True),
    ("image/jpg", MediaType.IMAGE, False),
    ("video/jpeg", MediaType.IMAGE, False),
    ("video/jpeg", None, False),
    ("/jpeg", None, False),
    ("video/mp4", None, True),
    ("video/mp4", MediaType.VIDEO, True),
    ("video/mp4", MediaType.IMAGE, False),
    (None, None, False),
    ("", None, False),
    (" ", None, False),
    (".jpeg", None, False),
]


@pytest.mark.parametrize("content_type, media_type, expected", IS_CONTENT_TYPE_ALLOWED)
def test_is_content_type_allowed(content_type, media_type, expected):
    """Test the is_content_type_allowed method for various scenarios."""
    assert MediaFormatUtils.is_content_type_allowed(content_type, media_type) == expected


# ===================== TESTS: get_extension =====================
GET_EXTNENSION_VALID = [
    (MediaType.IMAGE, Extension.JPEG, "jpeg"),
    (MediaType.VIDEO, Extension.MP4, "mp4"),
]


@pytest.mark.parametrize("media_type, extension, expected", GET_EXTNENSION_VALID)
def test_get_extension_valid(media_type, extension, expected):
    """Test valid combinations for the get_extension method."""
    assert MediaFormatUtils.get_extension(media_type, extension) == expected


GET_EXTNENSION_INVALID_TYPE = [
    (None, Extension.MP4),
    ("Image", Extension.JPEG),
    ("", Extension.JPEG),
    (" ", Extension.JPEG),
]


@pytest.mark.parametrize("media_type, extension", GET_EXTNENSION_INVALID_TYPE)
def test_get_extension_invalid_media_type(media_type, extension):
    """Test invalid media types for the get_extension method."""
    with pytest.raises(InvalidMediaTypeError):
        MediaFormatUtils.get_extension(media_type, extension)


GET_EXTNENSION_INVALID_EXTENSION = [
    (MediaType.IMAGE, "mp4"),
    (MediaType.IMAGE, Extension.MP4),
    (MediaType.VIDEO, Extension.JPEG),
    (MediaType.VIDEO, "mp4"),
    (MediaType.VIDEO, "jpg"),
    (MediaType.VIDEO, None),
    (MediaType.VIDEO, " "),
    (MediaType.VIDEO, ""),
]


@pytest.mark.parametrize("media_type, extension", GET_EXTNENSION_INVALID_EXTENSION)
def test_get_extension_invalid_extension(media_type, extension):
    """Test invalid extensions for the get_extension method."""
    with pytest.raises(InvalidExtensionError):
        MediaFormatUtils.get_extension(media_type, extension)


# ===================== TESTS: get_content_type =====================
GET_CONTENT_TYPE_VALID = [
    (MediaType.IMAGE, Extension.JPEG, "image/jpeg"),
    (MediaType.VIDEO, Extension.MP4, "video/mp4"),
]


@pytest.mark.parametrize("media_type, extension, expected", GET_CONTENT_TYPE_VALID)
def test_get_content_type_valid(media_type, extension, expected):
    """Test valid combinations for the get_content_type method."""
    assert MediaFormatUtils.get_content_type(media_type, extension) == expected


GET_CONTENT_TYPE_INVALID_TYPE = [
    (None, Extension.MP4),
    ("Image", Extension.JPEG),
    ("", Extension.JPEG),
    (" ", Extension.JPEG),
]


@pytest.mark.parametrize("media_type, extension", GET_CONTENT_TYPE_INVALID_TYPE)
def test_get_content_type_invalid_media_type(media_type, extension):
    """Test invalid media types for the get_content_type method."""
    with pytest.raises(InvalidMediaTypeError):
        MediaFormatUtils.get_content_type(media_type, extension)


# ===================== TESTS: map_extension_to_media_type =====================
MAP_EXT_TO_MEDIA_VALID = [
    (Extension.JPEG, MediaType.IMAGE),
    (Extension.MP4, MediaType.VIDEO),
]


@pytest.mark.parametrize("extension, expected", MAP_EXT_TO_MEDIA_VALID)
def test_map_extension_to_media_type_valid(extension, expected):
    """Test valid extensions for the map_extension_to_media_type method."""
    assert MediaFormatUtils.map_extension_to_media_type(extension) == expected


MAP_EXT_TO_MEDIA_INVALID = [
    ("jpg"),
    ("mp4"),
    (None),
    (" "),
    (""),
]


@pytest.mark.parametrize("extension", MAP_EXT_TO_MEDIA_INVALID)
def test_map_extension_to_media_type_invalid(extension):
    """Test invalid extensions for the map_extension_to_media_type method."""
    with pytest.raises(InvalidExtensionError):
        MediaFormatUtils.map_extension_to_media_type(extension)


# ===================== TESTS: extract_parts_from_content_type =====================
EXTRACT_FROM_CONTENT_VALID = [
    ("image/jpeg", "image", "jpeg"),
    ("video/mp4", "video", "mp4"),
]


@pytest.mark.parametrize(
    "content_type, expected_media, expected_extension", EXTRACT_FROM_CONTENT_VALID
)
def test_extract_parts_from_content_type_valid(content_type, expected_media, expected_extension):
    """Test valid extensions for the map_extension_to_media_type method."""
    media_type_str, extension_str = MediaFormatUtils.extract_parts_from_content_type(content_type)
    assert media_type_str == expected_media
    assert extension_str == expected_extension


EXTRACT_FROM_CONTENT_INVALID = [
    "jpeg",
    "/mp4",
    "mp4/",
    "image",
    "video",
    "",
    " ",
    None,
]


@pytest.mark.parametrize("content_type", EXTRACT_FROM_CONTENT_INVALID)
def test_extract_parts_from_content_type_invalid(content_type):
    """Test invalid extensions for the map_extension_to_media_type method."""
    with pytest.raises(InvalidContentTypeError):
        MediaFormatUtils.extract_parts_from_content_type(content_type)


# ===================== TESTS: convert_str_to_media_type =====================
CONVERT_STR_TO_MEDIA_VALID = [
    ("image", MediaType.IMAGE),
    ("video", MediaType.VIDEO),
]


@pytest.mark.parametrize("media_type_str, expected", CONVERT_STR_TO_MEDIA_VALID)
def test_convert_str_to_media_type_valid(media_type_str, expected):
    """Test valid strings for conversion to MediaType."""
    assert MediaFormatUtils.convert_str_to_media_type(media_type_str) == expected


CONVERT_STR_TO_MEDIA_INVALID = [
    ("jpeg"),
    ("mp4"),
    (""),
    (" "),
    None,
]


@pytest.mark.parametrize("media_type_str", CONVERT_STR_TO_MEDIA_INVALID)
def test_convert_str_to_media_type_invalid(media_type_str):
    """Test invalid strings for conversion to MediaType."""
    with pytest.raises(InvalidMediaTypeError):
        MediaFormatUtils.convert_str_to_media_type(media_type_str)


# ===================== TESTS: convert_str_to_extension =====================
CONVERT_STR_TO_EXT_VALID = [
    ("jpeg", Extension.JPEG),
    ("mp4", Extension.MP4),
]


@pytest.mark.parametrize("extension_str, expected", CONVERT_STR_TO_EXT_VALID)
def test_convert_str_to_extension_valid(extension_str, expected):
    """Test valid strings for conversion to Extension."""
    assert MediaFormatUtils.convert_str_to_extension(extension_str) == expected


CONVERT_STR_TO_EXT_INVALID = [
    ("image"),
    ("video"),
    (""),
    (" "),
    None,
]


@pytest.mark.parametrize("extension_str", CONVERT_STR_TO_EXT_INVALID)
def test_convert_str_to_extension_invalid(extension_str):
    """Test invalid strings for conversion to Extension."""
    with pytest.raises(InvalidExtensionError):
        MediaFormatUtils.convert_str_to_extension(extension_str)


# ===================== TESTS: parse_content_type =====================
PARSE_CONTENT_VALID = [
    ("image/jpeg", MediaType.IMAGE, Extension.JPEG),
    ("video/mp4", MediaType.VIDEO, Extension.MP4),
]


@pytest.mark.parametrize("content_type, expected_media, expected_extension", PARSE_CONTENT_VALID)
def test_parse_content_type_valid(content_type, expected_media, expected_extension):
    """Test valid content types for parsing."""
    media_type, extension = MediaFormatUtils.parse_content_type(content_type)
    assert media_type == expected_media
    assert extension == expected_extension


PARSE_CONTENT_INVALID = [
    ("jpeg"),
    ("/mp4"),
    ("mp4/"),
    ("image"),
    ("video"),
    (""),
    (" "),
    None,
]


@pytest.mark.parametrize("content_type", PARSE_CONTENT_INVALID)
def test_parse_content_type_invalid(content_type):
    """Test invalid content types for parsing."""
    with pytest.raises(InvalidContentTypeError):
        MediaFormatUtils.parse_content_type(content_type)
