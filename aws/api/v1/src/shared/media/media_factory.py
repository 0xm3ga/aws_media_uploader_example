from typing import Tuple

from shared.media.base import MediaFormatUtils
from shared.media.constants import EXTENSION_ALIAS_MAP, MediaType
from shared.media.image import ImageMedia
from shared.media.video import VideoMedia


class MediaFactory:
    @staticmethod
    def _parse_content_type(content_type: str) -> Tuple[str, str]:
        try:
            media_type, extension = content_type.split("/")
            extension = EXTENSION_ALIAS_MAP.get(extension.lower(), extension.lower())
        except Exception:
            raise ValueError("Invalid media type")

        return media_type, extension

    @staticmethod
    def _validate_content_type(content_type: str):
        if not MediaFormatUtils.is_content_type_allowed(content_type):
            raise ValueError("Invalid media type")

    @staticmethod
    def _validate_extension(extension: str):
        if not MediaFormatUtils.is_extension_allowed(extension):
            raise ValueError("Invalid extension")

    @staticmethod
    def create_media(content_type: str):
        # validating content type
        MediaFactory._validate_content_type(content_type)

        # parsing content type
        media_type, _ = MediaFactory._parse_content_type(content_type)

        # selecting media class
        if media_type == MediaType.IMAGE.value:
            return ImageMedia(content_type)
        elif media_type == MediaType.VIDEO.value:
            return VideoMedia(content_type)
        else:
            raise ValueError("Invalid media type")

    @staticmethod
    def create_media_from_extension(extension: str):
        # validating extension
        extension = EXTENSION_ALIAS_MAP.get(extension.lower(), extension.lower())
        MediaFactory._validate_extension(extension)

        # mapping extension to media type
        media_type = MediaFormatUtils.map_extension_to_media_type(extension)

        # constructing content type
        content_type = f"{media_type}/{extension}"

        # using the previous function to get the media instance
        return MediaFactory.create_media(content_type)


m = MediaFactory.create_media_from_extension("jpg")
print(m.content_type)
