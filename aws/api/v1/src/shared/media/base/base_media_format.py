from typing import Dict, Optional

from shared.media.constants import Extension, MediaType


class BaseMediaFormats:
    """Base media formats class."""

    NOT_IMPLEMENTED = "Subclasses should provide {value}"
    MEDIA_TYPE: Optional[MediaType] = None
    FORMATS: Dict[MediaType, Dict[Extension, str]] = {}

    @classmethod
    def init_formats(cls, media_type: MediaType, format_enum):
        """Initialize MEDIA_TYPE and FORMATS based on provided arguments."""
        cls.MEDIA_TYPE = media_type
        for item in format_enum:
            cls.FORMATS[item.name] = item.value

    @classmethod
    def _validate_formats(cls):
        if not cls.FORMATS:
            raise NotImplementedError(cls.NOT_IMPLEMENTED.format(value="FORMATS"))
