from typing import Set

from shared.media.constants import EXTENSION_ALIAS_MAP, FORMATS, Extension, MediaType


class MediaFormatUtils:
    @staticmethod
    def allowed_content_types():
        formats_dict = FORMATS

        """Get the allowed content types."""
        content_types: Set[str] = set()
        for media_type, formats in formats_dict.items():
            for extension in formats.values():
                content_types.add(f"{media_type.value}/{extension}")
        return content_types

    @staticmethod
    def allowed_extensions():
        """Get the allowed extensions."""
        return set(extensions.value for extensions in Extension)

    @staticmethod
    def is_extension_allowed(extension: str):
        """Check if an extension is allowed."""
        return (
            EXTENSION_ALIAS_MAP.get(extension.lower(), extension.lower())
            in MediaFormatUtils.allowed_extensions()
        )

    @staticmethod
    def is_content_type_allowed(content_type: str):
        """Check if a content type is allowed."""
        return content_type in MediaFormatUtils.allowed_content_types()

    @staticmethod
    def get_extension(
        media_type: MediaType,
        extension: Extension,
    ) -> str:
        return FORMATS[media_type][extension]

    @staticmethod
    def get_content_type(media_type: MediaType, extension: Extension):
        """Get the content type for the given format name."""
        return f"{media_type.value}/{MediaFormatUtils.get_extension(media_type, extension)}"
