import logging

from shared.constants.logging_messages import MediaMessages
from shared.exceptions import UnsupportedMediaTypeError
from shared.media.base import MediaFormatUtils, MediaType
from shared.media.constants import Extension, Size

from ..processors.image_processor import ImageProcessor
from ..processors.media_processor import MediaProcessor
from ..processors.video_processor import VideoProcessor

logger = logging.getLogger(__name__)


class MediaProcessorFactory:
    """Factory class for creating media processors."""

    @staticmethod
    def create_processor(
        bucket: str,
        key: str,
        filename: str,
        extension: Extension,
        sizes: list[Size],
        username: str,
    ) -> MediaProcessor:
        """
        Creates and returns an instance of the appropriate media processor based on the file type.
        """
        media_type = MediaFormatUtils.map_extension_to_media_type(extension)

        if media_type == MediaType.IMAGE:
            return ImageProcessor(bucket, key, filename, extension, sizes, username)
        elif media_type == MediaType.VIDEO:
            return VideoProcessor(bucket, key, filename, extension, sizes, username)
        else:
            logger.error(
                MediaMessages.Error.UNSUPPORTED_MEDIA_TYPE.format(media_type=media_type.value)
            )
            raise UnsupportedMediaTypeError(media_type=media_type.value)
