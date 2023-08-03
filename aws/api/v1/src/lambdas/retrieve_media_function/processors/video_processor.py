import logging
from typing import List

from media_processor import MediaProcessor
from shared.constants.media_constants import VideoFormat, VideoSize
from shared.exceptions import FeatureNotImplementedError

logger = logging.getLogger(__name__)


FEATURE_NAME = "Video processing"


class VideoProcessor(MediaProcessor):
    """Processor for video media."""

    def __init__(
        self,
        bucket: str,
        key: str,
        filename: str,
        format: VideoFormat,
        sizes: List[VideoSize],
        username: str,
    ):
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.image_format = format
        self.sizes = sizes
        self.username = username
        self.feature_name = FEATURE_NAME

    def process(self) -> dict:
        raise FeatureNotImplementedError(self.feature_name)
