from dataclasses import dataclass

from shared.media.base import BaseMediaFormats, MediaType
from shared.media.constants import FORMATS


class VideoFormats(BaseMediaFormats):
    MEDIA_TYPE = MediaType.VIDEO
    FORMATS = FORMATS[MEDIA_TYPE]

    @classmethod
    def get_media_type(cls) -> MediaType:
        if not cls.MEDIA_TYPE:
            raise
        return cls.MEDIA_TYPE


@dataclass
class VideoFormat:
    format: str

    @property
    def media_type(self):
        return VideoFormats.get_media_type().value

    @property
    def extension(self):
        return self.format

    def __str__(self):
        return f"VideoFormat(format={self.format}, media_type={self.media_type})"
