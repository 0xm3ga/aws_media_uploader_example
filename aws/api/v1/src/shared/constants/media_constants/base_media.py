from enum import Enum
from typing import Dict

EXTENSION_MAP: Dict[str, str] = {"jpg": "jpeg"}


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"

    @property
    def s3_prefix(self):
        return f"{self.value}s"


class BaseMediaFormat(Enum):
    @property
    def media_type(self):
        return self.value[0]

    @property
    def extension(self):
        return EXTENSION_MAP.get(self.value[1], self.value[1])

    @property
    def content_type(self):
        return f"{self.media_type}/{self.extension}"

    @classmethod
    def allowed_content_types(cls):
        return {format.content_type for format in cls}

    @classmethod
    def allowed_extensions(cls):
        return {format.name.lower() for format in cls}

    @classmethod
    def is_extension_allowed(cls, extension: str):
        return EXTENSION_MAP.get(extension.lower(), extension.lower()) in cls.allowed_extensions()

    @classmethod
    def is_content_type_allowed(cls, content_type: str):
        return content_type in cls.allowed_content_types()


class BaseMediaSize(Enum):
    @classmethod
    def allowed_sizes(cls):
        return {size.name for size in cls}

    @classmethod
    def allowed_dimensions(cls):
        return {size.value for size in cls}
