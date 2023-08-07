from typing import Dict

from shared.constants.error_messages import FeatureErrorMessages
from shared.media.constants import AspectRatio, DimensionData, Size


class BaseMediaSizes:
    """Base media sizes class."""

    DIMENSIONS: Dict[AspectRatio, Dict[Size, DimensionData]] = {}

    @classmethod
    def _validate_dimensions(cls):
        if not cls.DIMENSIONS:
            raise NotImplementedError(
                FeatureErrorMessages.FEATURE_NOT_IMPLEMENTED.format(feature_name="DIMENSIONS")
            )
