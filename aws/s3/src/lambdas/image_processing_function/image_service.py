import concurrent.futures
import logging
from typing import List

from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError
from enums import ImageFormat, ImageSize
from image_downloader import ImageDownloader
from image_media import ImageMedia
from image_processor import ImageProcessor
from image_uploader import ImageUploader
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

MAX_WORKERS = 5


class ImageService:
    def __init__(self, s3_client: BaseClient):
        self.s3_client = s3_client
        self.downloader = ImageDownloader(s3_client)
        self.processor = ImageProcessor()
        self.uploader = ImageUploader(s3_client)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(BotoCoreError),
    )
    def process_images(
        self,
        image_media: ImageMedia,
        processed_bucket: str,
        format: ImageFormat,
        sizes: List[ImageSize],
    ) -> None:
        download_path = None
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                download_path = self.downloader.download_image(image_media)

                self.processor.process_and_upload_images(
                    download_path,
                    image_media,
                    processed_bucket,
                    format,
                    sizes,
                    executor,
                    self.uploader,
                )
        except BotoCoreError as e:
            logger.exception(
                f"Error while interacting with AWSf S3: {e}, Image: {image_media.filename}"
            )
        except Exception as e:
            logger.exception(f"Unexpected error: {e}, Image: {image_media.filename}")
        finally:
            if download_path:
                self.downloader.cleanup(download_path)
