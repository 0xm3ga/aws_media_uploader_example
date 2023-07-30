import concurrent.futures
import logging
import uuid
from pathlib import Path
from typing import List

from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError
from enums import ImageFormat, ImageSize
from exceptions import ValidationError
from image_media import ImageMedia
from PIL import Image as PILImage
from PIL import ImageSequence
from pygifsicle import optimize
from s3_utils import download_file_from_s3, upload_file_to_s3
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

TEMP_DIR = Path("/tmp")

MAX_WORKERS = 5  # Replace this with a suitable number for your environment


def create_temp_path(filename: str, extension: str) -> Path:
    """
    Create a temporary path for a file with the given filename and extension.
    """
    return TEMP_DIR / f"{uuid.uuid4()}_{filename}.{extension}"


class ImageDownloader:
    def __init__(self, s3_client: BaseClient):
        self.s3_client = s3_client

    def download_image(self, image_media: ImageMedia) -> Path:
        download_path = create_temp_path(image_media.filename, image_media.extension)
        download_file_from_s3(self.s3_client, image_media.bucket, image_media.key, download_path)
        return download_path

    def cleanup(self, path: Path) -> None:
        path.unlink(missing_ok=True)


class ImageUploader:
    def __init__(self, s3_client: BaseClient):
        self.s3_client = s3_client

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def upload_image(self, new_path, processed_bucket, image_media, size, format):
        new_key = self._construct_new_key(image_media.filename, size, format)

        content_type = format.content_type
        upload_file_to_s3(self.s3_client, str(new_path), processed_bucket, new_key, content_type)
        new_path.unlink(missing_ok=True)

    def _construct_new_key(self, filename: str, size: ImageSize, format: ImageFormat) -> str:
        return f"{filename}/{size.name.lower()}.{format.value}"


class ImageProcessor:
    def process_and_upload_images(
        self,
        download_path: Path,
        image_media: ImageMedia,
        processed_bucket: str,
        format: ImageFormat,
        sizes: List[ImageSize],
        executor: concurrent.futures.Executor,
        uploader: ImageUploader,
    ) -> None:
        with PILImage.open(download_path) as img:
            try:
                self._resize_and_upload_images(
                    img, format, sizes, image_media, processed_bucket, executor, uploader
                )
            except ValidationError as e:
                logger.error(f"Validation Error: {e}")
                raise

    def _resize_and_upload_images(
        self,
        img: PILImage.Image,
        format: ImageFormat,
        sizes: List[ImageSize],
        image_media: ImageMedia,
        processed_bucket: str,
        executor: concurrent.futures.Executor,
        uploader: ImageUploader,
    ) -> None:
        futures = [
            executor.submit(
                self._resize_and_upload_image,
                size,
                format,
                img,
                image_media,
                processed_bucket,
                uploader,
            )
            for size in sizes
        ]
        concurrent.futures.wait(futures)

    def _resize_and_upload_image(
        self,
        size: ImageSize,
        format: ImageFormat,
        img: PILImage.Image,
        image_media: ImageMedia,
        processed_bucket: str,
        uploader: ImageUploader,
    ) -> None:
        new_filename = f"{image_media.filename}_{size.name.lower()}"
        new_extension = format.value
        local_path = create_temp_path(new_filename, new_extension)

        if format == ImageFormat.GIF:
            self._process_gif_image(img, size, format, local_path)
        else:
            self._process_other_images(img, size, format, local_path)

        try:
            uploader.upload_image(local_path, processed_bucket, image_media, size, format)
        except BotoCoreError as e:
            logger.error(f"Error while uploading to AWS S3: {e}")
            raise

    def _process_gif_image(self, new_size, new_path, img, format):
        frames = [frame.copy().resize(new_size) for frame in ImageSequence.Iterator(img)]
        frames[0].save(
            str(new_path),
            format=format.value,
            append_images=frames[1:],
            save_all=True,
            optimize=False,
        )
        optimize(str(new_path))

    def _process_other_images(
        self, img: PILImage.Image, size: ImageSize, format: ImageFormat, local_path: Path
    ):
        try:
            new_img = img.resize(size.value)
            new_img.save(local_path, format.value.upper())
        except Exception as e:
            print(f"ERROR: {e}")
            raise
        print("Image resized")


class ImageService:
    def __init__(self, s3_client: BaseClient):
        self.s3_client = s3_client
        self.downloader = ImageDownloader(s3_client)
        self.processor = ImageProcessor()
        self.uploader = ImageUploader(s3_client)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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
            logger.error(f"Error while interacting with AWS S3: {e}, Image: {image_media.filename}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}, Image: {image_media.filename}")
            raise
        finally:
            if download_path:
                self.downloader.cleanup(download_path)
