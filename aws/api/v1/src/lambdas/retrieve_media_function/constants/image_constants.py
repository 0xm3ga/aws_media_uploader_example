from enum import Enum
from typing import Dict


class ImageFormat(Enum):
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"

    @property
    def content_type(self):
        return "image/jpeg" if self.value == "jpg" else f"image/{self.value}"


class ImageSize(Enum):
    TINY = (120, 120)
    SMALL = (270, 270)
    MEDIUM = (540, 540)
    LARGE = (1080, 1080)
    HUGE = (2160, 2160)


ALLOWED_IMAGE_SIZES = {image_size.name.lower() for image_size in ImageSize}
ALLOWED_IMAGE_FORMATS = {image_format.name.lower() for image_format in ImageFormat}
ALLOWED_IMAGE_DIMENSIONS = {image_size.value for image_size in ImageSize}
ALLOWED_IMAGE_EXTENSIONS = {image_format.value for image_format in ImageFormat}

EXTENSION_MAP: Dict[str, str] = {"jpg": "jpeg"}
