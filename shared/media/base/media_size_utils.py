import logging
from typing import Optional, Set, Tuple

from shared.constants.logging_messages import MediaMessages
from shared.exceptions import InvalidAspectRatioError, InvalidMediaTypeError, InvalidSizeError
from shared.media.constants import (
    MEDIA_DIMENSIONS,
    AspectRatio,
    AspectRatioData,
    DimensionData,
    MediaType,
    Size,
)

logger = logging.getLogger(__name__)


class MediaSizeUtils:
    """Utility class for handling media sizes and related operations."""

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
        if size not in MediaSizeUtils.allowed_sizes():
            error_msg = MediaMessages.Error.UNSUPPORTED_SIZE.format(size=size)
            logger.error(error_msg)
            raise InvalidSizeError(error_msg)
        return True

    @staticmethod
    def is_aspect_ratio_allowed(aspect_ratio: AspectRatioData) -> bool:
        """Check if an aspect ratio is allowed."""
        if aspect_ratio not in MediaSizeUtils.allowed_aspect_ratios():
            error_msg = MediaMessages.Error.UNSUPPORTED_ASPECT_RATIO.format(
                aspect_ratio=aspect_ratio
            )
            logger.error(error_msg)
            raise InvalidAspectRatioError(error_msg)
        return True

    @staticmethod
    def allowed_dimensions(
        media_type: MediaType, aspect_ratio: Optional[AspectRatio] = None
    ) -> Set[DimensionData]:
        """Get the allowed dimensions."""
        if media_type not in MEDIA_DIMENSIONS:
            error_msg = MediaMessages.Error.UNSUPPORTED_MEDIA_TYPE.format(media_type=media_type)
            logger.error(error_msg)
            raise InvalidMediaTypeError(error_msg)

        if aspect_ratio and aspect_ratio not in MEDIA_DIMENSIONS[media_type]:
            error_msg = MediaMessages.Error.UNSUPPORTED_ASPECT_RATIO_FOR_MEDIA_TYPE.format(
                aspect_ratio=aspect_ratio, media_type=media_type
            )
            logger.error(error_msg)
            raise InvalidAspectRatioError(error_msg)

        dimensions_dict = (
            {aspect_ratio: MEDIA_DIMENSIONS[media_type][aspect_ratio]}
            if aspect_ratio
            else MEDIA_DIMENSIONS[media_type]
        )
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
        if media_type not in MEDIA_DIMENSIONS:
            error_msg = MediaMessages.Error.UNSUPPORTED_MEDIA_TYPE.format(media_type=media_type)
            logger.error(error_msg)
            raise InvalidMediaTypeError(error_msg)

        if aspect_ratio not in MEDIA_DIMENSIONS[media_type]:
            error_msg = MediaMessages.Error.UNSUPPORTED_ASPECT_RATIO_FOR_MEDIA_TYPE.format(
                aspect_ratio=aspect_ratio, media_type=media_type
            )
            logger.error(error_msg)
            raise InvalidAspectRatioError(error_msg)

        if size not in MEDIA_DIMENSIONS[media_type][aspect_ratio]:
            error_msg = MediaMessages.Error.UNSUPPORTED_SIZE_FOR_ASPECT_RATIO.format(
                size=size, aspect_ratio=aspect_ratio
            )
            logger.error(error_msg)
            raise InvalidSizeError(error_msg)

        return MEDIA_DIMENSIONS[media_type][aspect_ratio][size].as_tuple()

    # TODO: add unit tests
    @staticmethod
    def convert_str_to_size(size_str: str) -> Size:
        """
        Convert a media type string to its MediaType enum, raising an error for invalid strings.
        """
        try:
            size_str = str(size_str)
            return Size[size_str.upper()]
        except Exception:
            error_msg = MediaMessages.Error.UNSUPPORTED_SIZE.format(size_str=size_str)
            logger.error(error_msg)
            raise InvalidSizeError(error_msg)
