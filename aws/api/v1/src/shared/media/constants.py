from dataclasses import dataclass
from enum import Enum
from typing import Dict


@dataclass(frozen=True)
class AspectRatioData:
    width: int
    height: int

    def __str__(self):
        return f"{self.width}:{self.height}"

    def as_tuple(self):
        return self.width, self.height


@dataclass(frozen=True)
class DimensionData:
    width: int
    height: int

    def __str__(self):
        return f"{self.width}:{self.height}"

    def as_tuple(self):
        return self.width, self.height


EXTENSION_ALIAS_MAP: Dict[str, str] = {"jpg": "jpeg"}


class MediaType(Enum):
    """Media types supported."""

    IMAGE = "image"
    VIDEO = "video"


class Size(Enum):
    """Sizes supported."""

    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    HUGE = "huge"


class Extension(Enum):
    MP4 = "mp4"
    AVI = "avi"
    MOV = "mov"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"


class AspectRatio(Enum):
    """Aspect ratio supported."""

    AR_1_BY_1 = AspectRatioData(1, 1)
    AR_4_BY_5 = AspectRatioData(4, 5)
    AR_5_BY_4 = AspectRatioData(5, 4)
    AR_1_91_BY_1 = AspectRatioData(191, 100)
    AR_1_BY_1_91 = AspectRatioData(100, 191)


IMAGE_FORMATS = {
    Extension.JPEG: Extension.JPEG.value,
    Extension.PNG: Extension.PNG.value,
    Extension.GIF: Extension.GIF.value,
}

VIDEO_FORMATS = {
    Extension.MP4: Extension.MP4.value,
    Extension.MOV: Extension.MOV.value,
    Extension.AVI: Extension.AVI.value,
}

FORMATS = {
    MediaType.VIDEO: VIDEO_FORMATS,
    MediaType.IMAGE: IMAGE_FORMATS,
}


IMAGE_DIMENSIONS = {
    AspectRatio.AR_1_BY_1: {
        Size.TINY: DimensionData(120, 120),
        Size.SMALL: DimensionData(270, 270),
        Size.MEDIUM: DimensionData(540, 540),
        Size.LARGE: DimensionData(1080, 1080),
        Size.HUGE: DimensionData(2160, 2160),
    },
    AspectRatio.AR_4_BY_5: {
        Size.TINY: DimensionData(120, 150),
        Size.SMALL: DimensionData(270, 338),
        Size.MEDIUM: DimensionData(540, 675),
        Size.LARGE: DimensionData(1080, 1350),
        Size.HUGE: DimensionData(2160, 2700),
    },
    AspectRatio.AR_5_BY_4: {
        Size.TINY: DimensionData(150, 120),
        Size.SMALL: DimensionData(338, 270),
        Size.MEDIUM: DimensionData(675, 540),
        Size.LARGE: DimensionData(1350, 1080),
        Size.HUGE: DimensionData(2700, 2160),
    },
}

VIDEO_DIMENSIONS = {
    AspectRatio.AR_1_BY_1: {
        Size.TINY: DimensionData(120, 120),
        Size.SMALL: DimensionData(270, 270),
        Size.MEDIUM: DimensionData(540, 540),
        Size.LARGE: DimensionData(1080, 1080),
        Size.HUGE: DimensionData(2160, 2160),
    },
    AspectRatio.AR_4_BY_5: {
        Size.TINY: DimensionData(120, 150),
        Size.SMALL: DimensionData(270, 338),
        Size.MEDIUM: DimensionData(540, 675),
        Size.LARGE: DimensionData(1080, 1350),
        Size.HUGE: DimensionData(2160, 2700),
    },
    AspectRatio.AR_5_BY_4: {
        Size.TINY: DimensionData(150, 120),
        Size.SMALL: DimensionData(338, 270),
        Size.MEDIUM: DimensionData(675, 540),
        Size.LARGE: DimensionData(1350, 1080),
        Size.HUGE: DimensionData(2700, 2160),
    },
}

DIMENSIONS = {
    MediaType.IMAGE: IMAGE_DIMENSIONS,
    MediaType.VIDEO: VIDEO_DIMENSIONS,
}
