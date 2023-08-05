from typing import Optional, Set, Tuple

from shared.media.constants import (
    DIMENSIONS,
    AspectRatio,
    AspectRatioData,
    DimensionData,
    MediaType,
    Size,
)


class MediaSizeUtils:
    @staticmethod
    def allowed_sizes() -> Set[str]:
        """Get the allowed sizes."""
        return {size.value for size in Size}

    @staticmethod
    def allowed_aspect_ratios() -> Set[AspectRatioData]:
        """Get the allowed aspect ratios."""
        return {ratio.value for ratio in AspectRatio}

    @staticmethod
    def is_size_allowed(size: str) -> bool:
        """Check if a size is allowed."""
        return size in MediaSizeUtils.allowed_sizes()

    @staticmethod
    def is_aspect_ratio_allowed(aspect_ratio: AspectRatioData) -> bool:
        """Check if an aspect ratio is allowed."""
        return aspect_ratio in MediaSizeUtils.allowed_aspect_ratios()

    # TODO: review this
    @staticmethod
    def allowed_dimensions(
        media_type: MediaType, aspect_ratio: Optional[AspectRatio] = None
    ) -> Set[DimensionData]:
        """Get the allowed dimensions."""
        if aspect_ratio:
            dimensions_dict = {aspect_ratio: DIMENSIONS[media_type][aspect_ratio]}
        else:
            dimensions_dict = DIMENSIONS[media_type]

        dimensions: Set[DimensionData] = set()
        for _, sizes in dimensions_dict.items():
            for _, dimension in sizes.items():
                dimensions.add(dimension)
        return dimensions

    @staticmethod
    def get_dimensions(
        media_type: MediaType,
        aspect_ratio: AspectRatio,
        size: Size,
    ) -> Tuple[int, int]:
        return DIMENSIONS[media_type][aspect_ratio][size].as_tuple()
