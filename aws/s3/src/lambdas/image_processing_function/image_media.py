import logging

from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError
from utils import get_content_type, get_extension_from_content_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageMedia:
    def __init__(self, s3_client: BaseClient, bucket: str, key: str, filename: str):
        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.content_type = self._get_content_type()
        self.extension = self._get_extension()

    def _get_content_type(self) -> str:
        """Get content type of the image in the bucket."""
        try:
            return get_content_type(self.s3_client, self.bucket, self.key)
        except BotoCoreError as e:
            logger.error(f"Error getting content type of image from bucket: {e}")
            raise

    def _get_extension(self) -> str:
        """Get extension of the image."""
        try:
            return get_extension_from_content_type(self.content_type)
        except ValueError as e:
            logger.error(f"Error getting extension from content type: {e}")
            raise
