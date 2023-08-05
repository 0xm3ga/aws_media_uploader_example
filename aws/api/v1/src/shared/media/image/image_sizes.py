from typing import Tuple

from shared.media.base import BaseMediaSizes, MediaSizeUtils, MediaType
from shared.media.constants import IMAGE_DIMENSIONS, AspectRatio, Size


class ImageSizes(BaseMediaSizes):
    DIMENSIONS = IMAGE_DIMENSIONS


class ImageSize:
    FORMAT_STR = "ImageSize(aspect_ratio={aspect_ratio}, size={size}, dimension={dimension})"
    media_type = MediaType.IMAGE

    def __init__(self, aspect_ratio: AspectRatio, size: Size):
        self.aspect_ratio = aspect_ratio
        self.size = size

    @property
    def dimensions(self) -> Tuple[int, int]:
        return MediaSizeUtils.get_dimensions(
            media_type=self.media_type,
            aspect_ratio=self.aspect_ratio,
            size=self.size,
        )

    def __str__(self):
        return ImageSize.FORMAT_STR.format(
            aspect_ratio=self.aspect_ratio.value, size=self.size.value, dimension=self.dimensions
        )
