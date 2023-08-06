from dataclasses import dataclass

from shared.media.base import BaseMediaFormats, Extension, MediaFormatUtils, MediaType
from shared.media.constants import FORMATS


class VideoFormats(BaseMediaFormats):
    media_type = MediaType.VIDEO
    formats = FORMATS[MediaType.VIDEO]


@dataclass
class VideoFormat:
    FORMAT_STR = "VideoFormat(extension={extension}, content_type={content_type})"

    extension: Extension
    content_type: str
    media_type = MediaType.VIDEO

    def __str__(self):
        return self.FORMAT_STR.format(extension=self.extension, content_type=self.content_type)

    @classmethod
    def from_extension(cls, ext: str):
        MediaFormatUtils.is_extension_allowed(extension=ext, media_type=cls.media_type)
        extension = Extension[ext.upper()]
        return cls(extension=extension, content_type=f"{cls.media_type.value}/{extension.value}")

    @classmethod
    def from_content_type(cls, content_type: str):
        _, ext = content_type.split("/")
        MediaFormatUtils.is_extension_allowed(extension=ext, media_type=cls.media_type)
        extension = Extension[ext.upper()]
        return cls(extension=extension, content_type=f"{cls.media_type.value}/{extension.value}")


vfs = VideoFormats()
print(vfs.media_type)
