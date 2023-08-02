import logging
from typing import List

from exceptions import FeatureNotImplementedError
from media_processor import MediaProcessor

logger = logging.getLogger(__name__)


class VideoProcessor(MediaProcessor):
    """Processor for video media."""

    def __init__(
        self,
        bucket: str,
        key: str,
        filename: str,
        format: str,
        sizes: List[str],
        username: str,
    ):
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.image_format = format
        self.sizes = sizes
        self.username = username
        self.feature_name = "Video processing"

    def process(self) -> dict:
        raise FeatureNotImplementedError(self.feature_name)
