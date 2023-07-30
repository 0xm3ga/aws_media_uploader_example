import logging
from typing import List

from botocore.client import BaseClient
from enums import ImageFormat, ImageSize
from exceptions import ValidationError
from image_media import ImageMedia
from image_service import ImageService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AWSImageProcessingService:
    def __init__(self, s3_client: BaseClient, processed_bucket: str):
        self.s3_client = s3_client
        self.processed_bucket = processed_bucket
        self.image_service = ImageService(self.s3_client)

    def process_image(
        self, bucket: str, key: str, filename: str, format: ImageFormat, sizes: List[ImageSize]
    ):
        # Validate required fields, formats and sizes
        required_fields = ["bucket", "key", "filename", "format", "sizes"]
        ValidationError.check_required_fields(locals(), required_fields)
        ValidationError.check_value(format, ImageFormat, "format")
        ValidationError.check_subset(sizes, ImageSize, "sizes")

        # Create image media object for further processing
        image = ImageMedia(self.s3_client, bucket, key, filename)

        self.image_service.process_images(image, self.processed_bucket, format, sizes)
