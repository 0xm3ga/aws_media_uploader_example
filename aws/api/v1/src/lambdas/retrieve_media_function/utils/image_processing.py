import logging
from typing import List, Tuple

from constants.image_constants import ImageFormat, ImageSize

logger = logging.getLogger(__name__)


def validate_image_properties(size: str, extension: str) -> Tuple[List[str], str]:
    """Validates and returns the image size and format."""
    try:
        sizes = [ImageSize[size.upper()].name]
    except KeyError as e:
        logger.error(f"Invalid size provided: {e}")
        raise ValueError(f"Invalid size provided: {e}") from e

    try:
        image_format = ImageFormat[extension.upper()].name
    except KeyError as e:
        logger.error(f"Invalid format provided: {e}")
        raise ValueError(f"Invalid format provided: {e}") from e

    return sizes, image_format
