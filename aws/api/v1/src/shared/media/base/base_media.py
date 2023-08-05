from shared.media.constants import MediaType


class BaseMedia:
    """Base media class."""

    def __init__(self, media_type: MediaType):
        self.media_type = media_type

    @property
    def s3_prefix(self):
        return f"{self.media_type.value}s"
