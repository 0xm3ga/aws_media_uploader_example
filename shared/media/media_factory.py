import logging
from typing import Union

from shared.constants.logging_messages import MediaMessages
from shared.exceptions import InvalidContentTypeError, InvalidExtensionError
from shared.media.base import ImageMedia, MediaFormatUtils, VideoMedia
from shared.media.constants import MediaType


class MediaFactory:
    def __init__(self):
        self.media_format_utils = MediaFormatUtils()
        self.media_creators = {
            MediaType.IMAGE: ImageMedia,
            MediaType.VIDEO: VideoMedia,
        }

    @property
    def logger(self):
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(__name__ + "." + "MediaFactory")
        return self._logger

    def create_media_from_content_type(self, content_type: str) -> Union[ImageMedia, VideoMedia]:
        media_type, _ = self.media_format_utils.parse_content_type(content_type)
        media_class: Union[ImageMedia, VideoMedia] = self.media_creators.get(media_type, None)

        if not media_class:
            self.logger.error(
                MediaMessages.Error.INVALID_CONTENT_TYPE.format(content_type=content_type)
            )
            raise InvalidContentTypeError(content_type=content_type)
        return media_class

    def create_media_from_extension(self, extension_str: str) -> Union[ImageMedia, VideoMedia]:
        extension = self.media_format_utils.convert_str_to_extension(extension_str)
        media_type = self.media_format_utils.map_extension_to_media_type(extension)
        media_class: Union[ImageMedia, VideoMedia] = self.media_creators.get(media_type, None)

        if not media_class:
            self.logger.error(MediaMessages.Error.INVALID_EXTENSION.format(extension=extension_str))
            raise InvalidExtensionError
        return media_class
