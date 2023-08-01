import logging
from typing import List, Tuple

from constants.error_messages import INVALID_FORMAT_MSG, INVALID_SIZE_MSG
from constants.image_constants import ImageFormat, ImageSize
from exceptions import InvalidImageFormatError, InvalidImageSizeError

logger = logging.getLogger(__name__)


def validate_image_properties(size: str, extension: str) -> Tuple[List[str], str]:
    """Validates and returns the image size and format."""
    try:
        sizes = [ImageSize[size.upper()].name]
    except KeyError as e:
        logger.error(INVALID_SIZE_MSG.format(size=e))
        raise InvalidImageSizeError(size=str(e)) from e

    try:
        image_format = ImageFormat[extension.upper()].name
    except KeyError as e:
        logger.error(INVALID_FORMAT_MSG.format(extension=e))
        raise InvalidImageFormatError(extension=str(e)) from e

    return sizes, image_format
