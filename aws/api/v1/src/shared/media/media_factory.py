import logging
from typing import Union

from shared.constants.error_messages import MediaErrorMessages
from shared.exceptions import InvalidContentTypeError, InvalidExtensionError
from shared.media.base import MediaFormatUtils
from shared.media.constants import MediaType
from shared.media.image import ImageMedia
from shared.media.video import VideoMedia


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

    def create_media_from_content_type(
        self, content_type_str: str
    ) -> Union[ImageMedia, VideoMedia]:
        media_type, _ = self.media_format_utils.parse_content_type(content_type_str)
        media_class: Union[ImageMedia, VideoMedia] = self.media_creators.get(media_type, None)

        if not media_class:
            self.logger.error(MediaErrorMessages.INVALID_CONTENT_TYPE.format(content_type_str))
            raise InvalidContentTypeError
        return media_class

    def create_media_from_extension(self, extension_str: str) -> Union[ImageMedia, VideoMedia]:
        extension = self.media_format_utils.convert_str_to_extension(extension_str)
        media_type = self.media_format_utils.map_extension_to_media_type(extension)
        media_class: Union[ImageMedia, VideoMedia] = self.media_creators.get(media_type, None)

        if not media_class:
            self.logger.error(MediaErrorMessages.INVALID_EXTENSION.format(extension_str))
            raise InvalidExtensionError
        return media_class
