from typing import Tuple

from shared.media.base import MediaFormatUtils
from shared.media.constants import MediaType
from shared.media.image import ImageMedia
from shared.media.video import VideoMedia


class MediaFactory:
    @staticmethod
    def _parse_content_type(content_type: str) -> Tuple[str, str]:
        try:
            media_type, extension = content_type.split("/")
        except Exception:
            raise ValueError("Invalid media type")

        return media_type, extension

    @staticmethod
    def _validate_content_type(content_type: str):
        if content_type not in MediaFormatUtils.allowed_content_types():
            raise ValueError("Invalid media type")

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
