import logging
from typing import List

import exceptions as ex
from constants import error_messages as em
from constants.media_constants.file_types import FileType
from processors.image_processor import ImageProcessor
from processors.media_processor import MediaProcessor
from processors.video_processor import VideoProcessor

logger = logging.getLogger(__name__)


class MediaProcessorFactory:
    """Factory class for creating media processors."""

    @staticmethod
    def create_processor(
        bucket: str,
        key: str,
        filename: str,
        format: str,
        sizes: List[str],
        username: str,
        file_type: str,
    ) -> MediaProcessor:
        """
        Creates and returns an instance of the appropriate media processor based on the file type.
        """
        if file_type == FileType.IMAGE.value:
            return ImageProcessor(bucket, key, filename, format, sizes, username)
        elif file_type == FileType.VIDEO.value:
            return VideoProcessor(bucket, key, filename, format, sizes, username)
        else:
            logger.error(em.ERROR_UNSUPPORTED_FILE_TYPE_MSG.format(file_type))
            raise ex.UnsupportedFileTypeError(file_type)
