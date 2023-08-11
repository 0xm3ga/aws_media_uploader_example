import logging
from typing import List

from shared.exceptions import FeatureNotImplementedError
from shared.media.constants import Extension, Size

from .media_processor import MediaProcessor

logger = logging.getLogger(__name__)


FEATURE_NAME = "Video processing"


class VideoProcessor(MediaProcessor):
    """Processor for video media."""

    def __init__(
        self,
        bucket: str,
        key: str,
        filename: str,
        extension: Extension,
        sizes: List[Size],
        username: str,
    ):
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.extension = extension
        self.sizes = sizes
        self.username = username
        self.feature_name = FEATURE_NAME

    def process(self) -> dict:
        raise FeatureNotImplementedError(self.feature_name)
