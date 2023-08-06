from typing import Optional, Set

from shared.media.constants import FORMATS, Extension, MediaType


class MediaFormatUtils:
    @staticmethod
    def allowed_content_types(media_type: Optional[MediaType] = None):
        """Get the allowed content types."""
        if media_type:
            formats_dict = {media_type: FORMATS[media_type]}
        else:
            formats_dict = FORMATS

        content_types: Set[str] = set()
        for media_type, formats in formats_dict.items():
            for extension in formats.values():
                content_types.add(f"{media_type.value}/{extension}")
        return content_types

    @staticmethod
    def allowed_extensions(media_type: Optional[MediaType] = None) -> Set[str]:
        """Get the allowed extensions."""
        if media_type:
            formats_dict = {media_type: FORMATS[media_type]}
        else:
            formats_dict = FORMATS

        extensions: Set[str] = set()
        for media_type, formats in formats_dict.items():
            for extension in formats.values():
                extensions.add(extension)
        return extensions

    @staticmethod
    def is_extension_allowed(extension: str, media_type: Optional[MediaType] = None):
        """Check if an extension is allowed."""
        return extension in MediaFormatUtils.allowed_extensions(media_type=media_type)

    @staticmethod
    def is_content_type_allowed(content_type: str, media_type: Optional[MediaType] = None):
        """Check if a content type is allowed."""
        return content_type in MediaFormatUtils.allowed_content_types(media_type=media_type)

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

    @staticmethod
    def map_extension_to_media_type(extension: str) -> str:
        """Maps an extension to its corresponding media type value."""
        for media_type, extensions in FORMATS.items():
            if extension in extensions.values():
                return media_type.value
        raise ValueError("Invalid extension")
