from typing import Dict

from shared.media.constants import Extension, MediaType


class BaseMediaFormats:
    """Base media formats class."""

    NOT_IMPLEMENTED = "Subclasses should provide {value}"

    media_type: MediaType
    formats: Dict[Extension, str] = {}

    def __init__(self):
        """Initialize MEDIA_TYPE and FORMATS based on subclass."""
        if not self.formats:
            raise NotImplementedError(self.NOT_IMPLEMENTED.format(value="FORMATS"))

    def _validate_formats(self):
        if not self.formats:
            raise NotImplementedError(self.NOT_IMPLEMENTED.format(value="FORMATS"))
