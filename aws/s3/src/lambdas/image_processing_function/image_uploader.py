import logging
from pathlib import Path

from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError
from image_media import ImageMedia
from s3_utils import upload_file_to_s3
from tenacity import retry, stop_after_attempt, wait_exponential

from shared.media import Extension, Size
from shared.media.base import MediaFormatUtils

logger = logging.getLogger(__name__)


class ImageUploader:
    """A class to handle image uploads."""

    def __init__(self, s3_client: BaseClient):
        """Initialize the image uploader with an S3 client."""
        self.s3_client = s3_client

    class UploadFailed(Exception):
        """Raised when an image upload fails."""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def upload_image(
        self,
        new_path: Path,
        processed_bucket: str,
        image_media: ImageMedia,
        size: Size,
        extension: Extension,
    ) -> None:
        """Upload the image file to S3, retrying up to 3 times on failure."""
        new_key = self._construct_new_key(image_media.filename, size, extension)

        try:
            logger.info(f"Uploading image: {new_key} to bucket: {processed_bucket}")
            upload_file_to_s3(
                self.s3_client,
                new_path,
                processed_bucket,
                new_key,
                MediaFormatUtils.map_extension_to_media_type(extension=extension).value,
            )
            logger.info(f"Uploaded image: {new_key} to bucket: {processed_bucket}")
        except BotoCoreError as e:
            logger.error(
                f"Failed to upload image: {new_key} to bucket: {processed_bucket}, due to: {e}"
            )
            raise ImageUploader.UploadFailed from e
        finally:
            self.clean_up(new_path)

    def clean_up(self, new_path: Path) -> None:
        """
        Delete the file located at 'new_path' after upload, if it exists.
        """
        if new_path.exists():
            try:
                new_path.unlink(missing_ok=True)
                logger.info(f"Image file: {new_path} deleted after upload.")
            except OSError as e:
                logger.error(f"Error occurred while deleting image file: {new_path}, due to: {e}")
        else:
            logger.warning(f"Image file: {new_path} not found.")

    def _construct_new_key(self, filename: str, size: Size, extension: Extension) -> str:
        """Construct a new key based on the filename, size and format."""
        return f"{filename}/{size.name.lower()}.{extension.value}"
