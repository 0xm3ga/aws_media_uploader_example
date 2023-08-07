import logging
from typing import Optional, Set, Tuple

from shared.constants.error_messages import MediaErrorMessages
from shared.exceptions import InvalidContentTypeError, InvalidExtensionError, InvalidMediaTypeError
from shared.media.constants import EXTENSION_ALIAS_MAP, FORMATS, Extension, MediaType

logger = logging.getLogger(__name__)


class MediaFormatUtils:
    """Utility class for handling media formats and related operations."""

    @staticmethod
    def allowed_content_types(media_type: Optional[MediaType] = None) -> Set[str]:
        """Get the allowed content types for the specified media type."""
        if media_type and media_type not in FORMATS:
            error_msg = MediaErrorMessages.UNSUPPORTED_MEDIA_TYPE.format(
                media_type=media_type.value
            )
            logger.error(error_msg)
            raise InvalidMediaTypeError(error_msg)

        formats_dict = {media_type: FORMATS[media_type]} if media_type else FORMATS

        return {
            f"{m_type.value}/{ext}"
            for m_type, extensions in formats_dict.items()
            for ext in extensions.values()
        }

    @staticmethod
    def allowed_extensions(media_type: Optional[MediaType] = None) -> Set[str]:
        """Get the allowed extensions for the specified media type."""
        if media_type and media_type not in FORMATS:
            error_msg = MediaErrorMessages.UNSUPPORTED_MEDIA_TYPE.format(
                media_type=media_type.value
            )
            logger.error(error_msg)
            raise InvalidMediaTypeError(error_msg)

        formats_dict = {media_type: FORMATS[media_type]} if media_type else FORMATS

        return {ext for extensions in formats_dict.values() for ext in extensions.values()}

    @staticmethod
    def is_extension_allowed(extension: str, media_type: Optional[MediaType] = None) -> bool:
        """Return whether a given extension is allowed for the specified media type."""
        return extension in MediaFormatUtils.allowed_extensions(media_type=media_type)

    @staticmethod
    def is_content_type_allowed(content_type: str, media_type: Optional[MediaType] = None) -> bool:
        """Return whether a given content type is allowed for the specified media type."""
        return content_type in MediaFormatUtils.allowed_content_types(media_type=media_type)

    @staticmethod
    def get_extension(media_type: MediaType, extension: Extension) -> str:
        """Retrieve the file extension for the specified media type and format name."""
        if media_type not in FORMATS:
            error_msg = MediaErrorMessages.UNSUPPORTED_MEDIA_TYPE.format(
                media_type=media_type.value
            )
            logger.error(error_msg)
            raise InvalidMediaTypeError(error_msg)
        if extension not in FORMATS[media_type]:
            error_msg = MediaErrorMessages.INVALID_EXTENSION.format(extension=extension.value)
            logger.error(error_msg)
            raise InvalidExtensionError(error_msg)

        return FORMATS[media_type][extension]

    @staticmethod
    def get_content_type(media_type: MediaType, extension: Extension) -> str:
        """Return the content type for the given media type and format name."""
        return f"{media_type.value}/{MediaFormatUtils.get_extension(media_type, extension)}"

    @staticmethod
    def map_extension_to_media_type(extension: Extension) -> MediaType:
        """
        Map an extension to its corresponding media type. Raises ValueError for invalid extensions.
        """
        for media_type, extensions in FORMATS.items():
            if extension in extensions:
                return media_type

        error_msg = MediaErrorMessages.INVALID_EXTENSION.format(extension=extension.value)
        logger.error(error_msg)
        raise InvalidExtensionError(error_msg)

    @staticmethod
    def extract_parts_from_content_type(content_type: str) -> Tuple[str, str]:
        """Extract media type and extension strings from a content type."""
        if not content_type:
            logger.error(MediaErrorMessages.EMPTY_CONTENT_TYPE)
            raise ValueError(MediaErrorMessages.EMPTY_CONTENT_TYPE)

        try:
            media_type_str, extension_str = content_type.split("/")
            return media_type_str, extension_str
        except ValueError:
            error_msg = MediaErrorMessages.INVALID_CONTENT_TYPE.format(content_type=content_type)
            logger.error(error_msg)
            raise InvalidContentTypeError(error_msg)

    @staticmethod
    def convert_str_to_media_type(media_type_str: str) -> MediaType:
        """
        Convert a media type string to its MediaType enum, raising an error for invalid strings.
        """
        try:
            return MediaType[media_type_str.upper()]
        except Exception:
            error_msg = MediaErrorMessages.UNSUPPORTED_MEDIA_TYPE.format(media_type=media_type_str)
            logger.error(error_msg)
            raise InvalidMediaTypeError(error_msg)

    @staticmethod
    def convert_str_to_extension(extension_str: str) -> Extension:
        """
        Convert an extension string to its Extension enum, raising an error for invalid strings.
        """
        extension_str = EXTENSION_ALIAS_MAP.get(extension_str.lower(), extension_str.lower())
        try:
            return Extension[extension_str.upper()]
        except Exception:
            error_msg = MediaErrorMessages.INVALID_EXTENSION.format(extension=extension_str)
            logger.error(error_msg)
            raise InvalidExtensionError(error_msg)

    @staticmethod
    def parse_content_type(content_type: str) -> Tuple[MediaType, Extension]:
        """Parse a content type into its corresponding MediaType and Extension enums."""
        try:
            media_type_str, extension_str = MediaFormatUtils.extract_parts_from_content_type(
                content_type
            )
            media_type = MediaFormatUtils.convert_str_to_media_type(media_type_str)
            extension = MediaFormatUtils.convert_str_to_extension(extension_str)

            return media_type, extension
        except Exception:
            error_msg = MediaErrorMessages.INVALID_CONTENT_TYPE.format(content_type=content_type)
            logger.error(error_msg)
            raise InvalidContentTypeError(error_msg)
