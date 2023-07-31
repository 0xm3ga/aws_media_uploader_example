from enum import Enum
from typing import Dict


class FileType(Enum):
    IMAGE = "images"
    VIDEO = "videos"


class ImageFormat(Enum):
    """
    Enum to represent allowed image formats
    """

    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"

    @property
    def content_type(self):
        return "image/jpeg" if self.value == "jpg" else f"image/{self.value}"


class ImageSize(Enum):
    """
    Enum to represent allowed image sizes
    """

    TINY = (120, 120)
    SMALL = (270, 270)
    MEDIUM = (540, 540)
    LARGE = (1080, 1080)
    HUGE = (2160, 2160)


ALLOWED_IMAGE_SIZES = set(ImageSize.__members__.keys())
ALLOWED_IMAGE_FORMATS = set(ImageFormat.__members__.keys())

ALLOWED_IMAGE_DIMENSIONS = {image_format.value for image_format in ImageSize}
ALLOWED_IMAGE_EXTENSIONS = {image_format.value for image_format in ImageFormat}

EXTENSION_MAP: Dict[str, str] = {"jpg": "jpeg"}


ACCEPTED_SIZES = ["tiny", "small", "medium", "large", "huge"]
ACCEPTED_FORMATS = ["jpg", "jpeg", "png", "gif", "mp4"]
