from enum import Enum
from typing import Dict


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

    SMALL = (300, 300)
    MEDIUM = (600, 600)
    LARGE = (1200, 1200)


ALLOWED_IMAGE_FORMATS = set(ImageFormat.__members__.keys())
ALLOWED_IMAGE_SIZES = set(ImageSize.__members__.keys())

ALLOWED_IMAGE_EXTENSIONS = {image_format.value for image_format in ImageFormat}

EXTENSION_MAP: Dict[str, str] = {"jpg": "jpeg"}
