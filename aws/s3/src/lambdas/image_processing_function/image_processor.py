import concurrent.futures
import logging
from pathlib import Path
from typing import List

from botocore.exceptions import BotoCoreError
from enums import ImageFormat, ImageSize
from image_media import ImageMedia
from image_uploader import ImageUploader
from PIL import Image as PILImage
from PIL import ImageSequence, UnidentifiedImageError
from pygifsicle import optimize
from utils import create_temp_path

logger = logging.getLogger(__name__)

MAX_WORKERS = 5


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
        try:
            self._resize_and_upload_images(
                download_path, format, sizes, image_media, processed_bucket, executor, uploader
            )
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            raise

    def _create_pil_image(self, download_path: Path) -> PILImage.Image:
        try:
            return PILImage.open(download_path)
        except UnidentifiedImageError as e:
            logger.exception(f"Error opening image file: {e}")
            raise

    def _resize_and_upload_images(
        self,
        download_path: Path,
        format: ImageFormat,
        sizes: List[ImageSize],
        image_media: ImageMedia,
        processed_bucket: str,
        executor: concurrent.futures.Executor,
        uploader: ImageUploader,
    ) -> None:
        futures = [
            executor.submit(
                self._resize_and_upload_single_image,
                size,
                format,
                download_path,
                image_media,
                processed_bucket,
                uploader,
            )
            for size in sizes
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    def _resize_and_upload_single_image(
        self,
        size: ImageSize,
        format: ImageFormat,
        download_path: Path,
        image_media: ImageMedia,
        processed_bucket: str,
        uploader: ImageUploader,
    ) -> None:
        img = self._create_pil_image(download_path)
        new_filename = f"{image_media.filename}_{size.name.lower()}"
        new_extension = format.value
        local_path = create_temp_path(new_filename, new_extension)

        try:
            if format == ImageFormat.GIF:
                self._process_gif_image(img, size, format, local_path)
            else:
                self._process_other_images(img, size, format, local_path)

            uploader.upload_image(local_path, processed_bucket, image_media, size, format)
        except BotoCoreError as e:
            logger.error(f"Error while uploading to AWS S3: {e}")
            raise
        finally:
            if local_path.exists():
                local_path.unlink()

    def _process_gif_image(
        self, img: PILImage.Image, size: ImageSize, format: ImageFormat, local_path: Path
    ):
        try:
            frames = [frame.copy().resize(size.value) for frame in ImageSequence.Iterator(img)]
            frames[0].save(
                str(local_path),
                format=format.value,
                append_images=frames[1:],
                save_all=True,
                optimize=False,
            )
            optimize(str(local_path))
        except Exception as e:
            logger.error(f"Unexpected error while processing GIF image: {e}")
            raise

    def _process_other_images(
        self, img: PILImage.Image, size: ImageSize, format: ImageFormat, local_path: Path
    ):
        try:
            new_img = img.resize(size.value)
            new_img.save(local_path, format.value.upper())
        except OSError as e:
            logger.error(f"Corrupted image: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while resizing image: {e}")
            raise
