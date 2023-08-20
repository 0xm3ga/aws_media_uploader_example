from shared.media.base import BaseMedia, MediaType


class ImageMedia(BaseMedia):
    def __init__(self, content_type):
        self.content_type = content_type
        super().__init__(media_type=MediaType.IMAGE)
