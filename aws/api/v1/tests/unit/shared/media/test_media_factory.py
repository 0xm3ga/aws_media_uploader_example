from unittest.mock import patch

import pytest

from aws.api.v1.src.shared.media.media_factory import (
    ImageMedia,
    InvalidContentTypeError,
    InvalidExtensionError,
    MediaFactory,
    MediaMessages,
    MediaType,
    VideoMedia,
)

# ===================== CONSTANTS =====================
SUPPORTED_CONTENT_TYPES = [
    ("image/png", ImageMedia, MediaType.IMAGE),
    ("image/jpeg", ImageMedia, MediaType.IMAGE),
    ("image/gif", ImageMedia, MediaType.IMAGE),
    ("video/mp4", VideoMedia, MediaType.VIDEO),
    ("video/mov", VideoMedia, MediaType.VIDEO),
    ("video/avi", VideoMedia, MediaType.VIDEO),
]

INVALID_CONTENT_TYPES = [
    "text/plain",
    "application/json",
    "randomtype/randomsubtype",
    "/jpeg",
    "image/video",
    "viode/jpeg",
    "video/",
    "images/jpeg",
    " ",
    "",
    "/",
    " /",
    "/ ",
    None,
]

SUPPORTED_EXTENSIONS = [
    ("png", ImageMedia, MediaType.IMAGE),
    ("jpg", ImageMedia, MediaType.IMAGE),
    ("jpeg", ImageMedia, MediaType.IMAGE),
    ("gif", ImageMedia, MediaType.IMAGE),
    ("mp4", VideoMedia, MediaType.VIDEO),
    ("mov", VideoMedia, MediaType.VIDEO),
    ("avi", VideoMedia, MediaType.VIDEO),
]

INVALID_EXTENSIONS = [
    "txt",
    "json",
    "random",
    "",
    None,
    " ",
    "...",
]


# ===================== FIXTURES =====================
@pytest.fixture
def media_factory():
    """Fixture to provide an instance of MediaFactory for tests."""
    return MediaFactory()


# ===================== TESTS: CONTENT TYPES =====================
@pytest.mark.parametrize("content_type, expected_class, media_type", SUPPORTED_CONTENT_TYPES)
def test_create_media_from_content_type_valid(
    media_factory, content_type, expected_class, media_type
):
    """
    Test valid content types.
    Ensure correct media class is created for supported content types.
    """
    with patch(
        "aws.api.v1.src.shared.media.media_factory.MediaFormatUtils.parse_content_type",
        return_value=(media_type, None),
    ):
        media_class = media_factory.create_media_from_content_type(content_type)
        assert media_class == expected_class


@pytest.mark.parametrize("invalid_content_type", INVALID_CONTENT_TYPES)
def test_create_media_from_content_type_invalid(media_factory, invalid_content_type):
    """
    Test invalid content types.
    Ensure an error is raised when using unsupported or malformed content types.
    """
    with patch(
        "aws.api.v1.src.shared.media.media_factory.MediaFormatUtils.parse_content_type",
        return_value=(None, None),
    ):
        with pytest.raises(InvalidContentTypeError) as exception_info:
            media_factory.create_media_from_content_type(invalid_content_type)
            assert str(exception_info.value) == MediaMessages.Error.INVALID_CONTENT_TYPE.format(
                content_type=invalid_content_type
            )


# ===================== TESTS: FILE EXTENSIONS =====================
@pytest.mark.parametrize("extension, expected_class, media_type", SUPPORTED_EXTENSIONS)
def test_create_media_from_extension_valid(media_factory, extension, expected_class, media_type):
    """
    Test valid file extensions.
    Ensure correct media class is created for supported file extensions.
    """
    with patch(
        "aws.api.v1.src.shared.media.media_factory.MediaFormatUtils.convert_str_to_extension",
        return_value=extension,
    ), patch(
        "aws.api.v1.src.shared.media.media_factory.MediaFormatUtils.map_extension_to_media_type",
        return_value=media_type,
    ):
        media_class = media_factory.create_media_from_extension(extension)
        assert media_class == expected_class


@pytest.mark.parametrize("invalid_extension", INVALID_EXTENSIONS)
def test_create_media_from_extension_invalid(media_factory, invalid_extension):
    """
    Test invalid file extensions.
    Ensure an error is raised when using unsupported or malformed file extensions.
    """
    with patch(
        "aws.api.v1.src.shared.media.media_factory.MediaFormatUtils.convert_str_to_extension",
        return_value=invalid_extension,
    ), patch(
        "aws.api.v1.src.shared.media.media_factory.MediaFormatUtils.map_extension_to_media_type",
        return_value=None,
    ):
        with pytest.raises(InvalidExtensionError) as exception_info:
            media_factory.create_media_from_extension(invalid_extension)
            assert str(exception_info.value) == MediaMessages.Error.INVALID_EXTENSION.format(
                extension=invalid_extension
            )


# ===================== TESTS: LOGGER =====================
# Logger tests
def test_logger(media_factory):
    """
    Test logger instantiation.
    Ensure logger is correctly initialized within the MediaFactory.
    """
    with patch("aws.api.v1.src.shared.media.media_factory.logging.getLogger") as mock_get_logger:
        logger = media_factory.logger
        mock_get_logger.assert_called_once_with(
            "aws.api.v1.src.shared.media.media_factory.MediaFactory"
        )
        assert logger == media_factory._logger
