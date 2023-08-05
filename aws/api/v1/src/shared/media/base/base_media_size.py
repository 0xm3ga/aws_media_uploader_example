from typing import Dict

from shared.media.constants import AspectRatio, DimensionData, Size


class BaseMediaSizes:
    """Base media sizes class."""

    NOT_IMPLEMENTED = "Subclasses should provide {value}"
    DIMENSIONS: Dict[AspectRatio, Dict[Size, DimensionData]] = {}

    @classmethod
    def _validate_dimensions(cls):
        if not cls.DIMENSIONS:
            raise NotImplementedError(cls.NOT_IMPLEMENTED.format(value="DIMENSIONS"))
