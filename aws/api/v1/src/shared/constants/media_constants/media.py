import logging
from typing import Any, Set

from shared.constants.error_messages import ProcessingErrorMessages
from shared.constants.media_constants import ImageFormat, ImageSize, VideoFormat, VideoSize
from shared.exceptions import InvalidParameterError, UnsupportedExtensionError, UnsupportedSizeError

logging.basicConfig(level=logging.DEBUG)


class MediaFormat:
    logger = logging.getLogger(__name__)

    @staticmethod
    def allowed_extensions() -> Set[str]:
        image_allowed_extensions = ImageFormat.allowed_extensions()
        video_allowed_extensions = VideoFormat.allowed_extensions()
        allowed_extensions = set.union(image_allowed_extensions, video_allowed_extensions)
        return allowed_extensions

    @staticmethod
    def allowed_content_types() -> Set[str]:
        image_allowed_content_types = ImageFormat.allowed_content_types()
        video_allowed_content_types = VideoFormat.allowed_content_types()
        allowed_content_types = set.union(image_allowed_content_types, video_allowed_content_types)
        return allowed_content_types

    @staticmethod
    def _clean_up_input(value: Any) -> str:
        try:
            return str(value).strip().lower()
        except Exception as e:
            logging.error(ProcessingErrorMessages.INVALID_PARAMETER, e)
            raise InvalidParameterError(str(e))

    @classmethod
    def is_extension_allowed(cls, extension: str) -> bool:
        extension = cls._clean_up_input(extension)
        return ImageFormat.is_extension_allowed(extension) or VideoFormat.is_extension_allowed(
            extension
        )

    @classmethod
    def validate_extension(cls, extension: str):
        extension = cls._clean_up_input(extension)
        if not cls.is_extension_allowed(extension):
            raise UnsupportedExtensionError(extension)
        return extension


class MediaSize:
    @staticmethod
    def allowed_sizes():
        image_allowed_sizes = ImageSize.allowed_sizes()
        video_allowed_sizes = VideoSize.allowed_sizes()
        allowed_sizes = set.union(image_allowed_sizes, video_allowed_sizes)
        return allowed_sizes

    @staticmethod
    def allowed_dimensions():
        image_allowed_dimensions = ImageSize.allowed_dimensions()
        video_allowed_dimensions = VideoSize.allowed_dimensions()
        allowed_dimensions = set.union(image_allowed_dimensions, video_allowed_dimensions)
        return allowed_dimensions

    @staticmethod
    def _clean_up_input(value: Any) -> str:
        try:
            return str(value).strip().lower()
        except Exception as e:
            logging.error(ProcessingErrorMessages.INVALID_PARAMETER, e)
            raise InvalidParameterError(str(e))

    @classmethod
    def is_size_allowed(cls, size: str) -> bool:
        size = cls._clean_up_input(size)
        return ImageSize.is_size_allowed(size) or VideoSize.is_size_allowed(size)

    @classmethod
    def validate_size(cls, size: str):
        size = cls._clean_up_input(size)
        if not cls.is_size_allowed(size):
            raise UnsupportedSizeError(size)
        return size
