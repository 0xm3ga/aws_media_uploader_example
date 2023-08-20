from shared.media.constants import MediaType


class BaseMedia:
    """Base media class to represent a generic media type."""

    def __init__(self, media_type: MediaType):
        """
        Initialize a BaseMedia instance.
        """
        self._media_type = media_type

    @property
    def s3_prefix(self) -> str:
        """
        Construct and return the prefix to be used in S3 based on the media type.
        """
        return f"{self._media_type.value}s"
