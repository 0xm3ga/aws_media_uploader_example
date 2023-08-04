from enum import Enum
from typing import Dict, Set


class MediaType(Enum):
    """Media types supported."""

    IMAGE = "image"
    VIDEO = "video"


class BaseMedia:
    """Base media class."""

    def __init__(self, media_type: MediaType):
        self.media_type = media_type

    @property
    def s3_prefix(self):
        return f"{self.media_type.value}s"


EXTENSION_ALIAS_MAP: Dict[str, str] = {"jpg": "jpeg"}


class BaseMediaFormat(Enum):
    """Base media format class."""

    @property
    def media_type(self):
        return self.value[0]

    @property
    def extension(self):
        """Get the extension."""
        return EXTENSION_ALIAS_MAP.get(self.value[1], self.value[1])

    @property
    def content_type(self):
        """Get the content type."""
        return f"{self.media_type}/{self.extension}"

    @classmethod
    def allowed_content_types(cls):
        """Get the allowed content types."""
        return {format.content_type for format in cls}

    @classmethod
    def allowed_extensions(cls) -> Set[str]:
        """Get the allowed extensions."""
        return {format.name.lower() for format in cls}

    @classmethod
    def is_extension_allowed(cls, extension: str):
        """Check if an extension is allowed."""
        return (
            EXTENSION_ALIAS_MAP.get(extension.lower(), extension.lower())
            in cls.allowed_extensions()
        )

    @classmethod
    def is_content_type_allowed(cls, content_type: str):
        """Check if a content type is allowed."""
        return content_type in cls.allowed_content_types()


class BaseMediaSize(Enum):
    @classmethod
    def allowed_sizes(cls):
        """Get the allowed sizes."""
        return {size.name.lower() for size in cls}

    @classmethod
    def allowed_dimensions(cls):
        """Get the allowed dimensions."""
        return {size.value for size in cls}

    @classmethod
    def is_size_allowed(cls, size: str):
        """Check if a size is allowed."""
        return size in cls.allowed_sizes()
