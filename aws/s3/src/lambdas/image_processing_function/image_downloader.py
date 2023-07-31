import logging
from pathlib import Path

from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError
from image_media import ImageMedia
from s3_utils import download_file_from_s3
from utils import create_temp_path

# from contextlib import contextmanager
# from typing import Generator


logger = logging.getLogger(__name__)


class ImageDownloader:
    """
    A class to handle downloading images from an S3 bucket.
    """

    def __init__(self, s3_client: BaseClient):
        """
        Initialize the image downloader with an S3 client.
        """
        self.s3_client = s3_client

    def download_image(self, image_media: ImageMedia) -> Path:
        """
        Download the image from the S3 bucket.
        """
        download_path = create_temp_path(image_media.filename, image_media.extension)
        try:
            download_file_from_s3(
                self.s3_client,
                image_media.bucket,
                image_media.key,
                download_path,
            )
            logger.info(f"Downloaded image: {download_path}")
            return download_path
        except BotoCoreError as e:
            logger.error(f"Failed to download image: {image_media.filename}, due to: {e}")
            raise

    def cleanup(self, path: Path) -> None:
        """
        Cleanup the temporary downloaded image file.
        """
        try:
            path.unlink(missing_ok=True)
            logger.info(f"Cleaned up image file: {path}")
        except Exception as e:
            logger.error(f"Failed to cleanup image file: {path}, due to: {e}")
            raise
