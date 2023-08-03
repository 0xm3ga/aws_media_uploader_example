import logging

import shared.exceptions as ex
from processors.image_processor import ImageProcessor
from processors.media_processor import MediaProcessor
from processors.video_processor import VideoProcessor
from shared.constants.error_messages import LambdaErrorMessages
from shared.constants.media_constants import (
    ImageFormat,
    ImageSize,
    MediaType,
    VideoFormat,
    VideoSize,
)

logger = logging.getLogger(__name__)


class MediaProcessorFactory:
    """Factory class for creating media processors."""

    @staticmethod
    def create_processor(
        bucket: str,
        key: str,
        filename: str,
        extension: str,
        sizes: list[str],
        username: str,
        media_type: MediaType,
    ) -> MediaProcessor:
        """
        Creates and returns an instance of the appropriate media processor based on the file type.
        """
        if media_type == MediaType.IMAGE:
            image_sizes = [ImageSize[size] for size in sizes]
            format = ImageFormat[extension]
            return ImageProcessor(bucket, key, filename, format, image_sizes, username)
        elif media_type == MediaType.VIDEO:
            video_sizes = [VideoSize[size] for size in sizes]
            format = VideoFormat[extension]
            return VideoProcessor(bucket, key, filename, format, video_sizes, username)
        else:
            logger.error(LambdaErrorMessages.ERROR_UNSUPPORTED_FILE_TYPE.format(media_type.value))
            raise ex.UnsupportedFileTypeError(media_type.value)
