from dataclasses import dataclass

from shared.media.base import BaseMediaFormats, Extension, MediaFormatUtils, MediaType
from shared.media.constants import FORMATS


class ImageFormats(BaseMediaFormats):
    media_type = MediaType.IMAGE
    format = FORMATS[MediaType.IMAGE]


@dataclass
class ImageFormat:
    FORMAT_STR = "ImageFormat(extension={extension}, content_type={content_type})"

    extension: Extension
    content_type: str
    media_type = MediaType.IMAGE

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
