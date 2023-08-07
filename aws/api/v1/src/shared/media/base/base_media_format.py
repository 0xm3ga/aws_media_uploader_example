from typing import Dict

from shared.constants.error_messages import FeatureErrorMessages
from shared.media.constants import Extension, MediaType


class BaseMediaFormats:
    """Base media formats class."""

    media_type: MediaType
    formats: Dict[Extension, str] = {}

    def __init__(self):
        """Initialize MEDIA_TYPE and FORMATS based on subclass."""
        if not self.formats:
            raise NotImplementedError(
                FeatureErrorMessages.FEATURE_NOT_IMPLEMENTED.format(feature_name="FORMATS")
            )

    def _validate_formats(self):
        if not self.formats:
            raise NotImplementedError(
                FeatureErrorMessages.FEATURE_NOT_IMPLEMENTED.format(feature_name="FORMATS")
            )
