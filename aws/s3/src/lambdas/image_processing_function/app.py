import logging
import mimetypes
import os
import uuid
from enum import Enum
from pathlib import Path

import boto3
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageFormat(Enum):
    JPEG = "jpg"
    PNG = "png"
    GIF = "gif"


class ImageSize(Enum):
    SMALL = (300, 300)
    MEDIUM = (600, 600)
    LARGE = (1200, 1200)


class UnsupportedImageFormatError(Exception):
    pass


class ImageMedia:
    def __init__(self, s3_client, bucket, key):
        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        self.content_type = self._get_content_type()
        self.extension = self._get_extension()
        self.username, self.filetype, self.filename = self._parse_key()

    def _get_content_type(self):
        response = self.s3_client.head_object(Bucket=self.bucket, Key=self.key)
        return response["ContentType"]

    def _get_extension(self):
        extension = mimetypes.guess_extension(self.content_type)
        if extension is None:
            raise UnsupportedImageFormatError(
                f"Unable to guess extension for content type: {self.content_type}"
            )
        extension = extension.lstrip(".")
        if extension not in [image_format.value for image_format in ImageFormat]:
            raise UnsupportedImageFormatError(f"Unsupported image format: {extension}")
        return extension

    def _parse_key(self):
        parts = self.key.split("/")
        if len(parts) != 3:
            raise ValueError(f"Unexpected key format: {self.key}")
        return parts[0], parts[1], parts[2]


class ImageProcessor:
    def __init__(self, s3_client):
        self.s3_client = s3_client

    def download_image(self, image_media):
        self.download_path = Path("/tmp") / f"{uuid.uuid4()}.{image_media.extension}"
        self.download_path.parent.mkdir(parents=True, exist_ok=True)
        self.s3_client.download_file(image_media.bucket, image_media.key, str(self.download_path))

    def process_image(self, image_media):
        self.upload_paths = {}

        with Image.open(self.download_path) as img:
            for size in ImageSize:
                for image_format in ImageFormat:
                    new_size = size.value
                    new_path = (
                        Path("/tmp")
                        / f"{image_media.filename}-{size.name.lower()}.{image_format.value}"
                    )
                    new_img = img.resize(new_size)
                    new_img.save(
                        str(new_path),
                        "JPEG" if image_format.value == "jpg" else image_format.value.upper(),
                    )

                    self.upload_paths[(size.name.lower(), image_format.value)] = new_path

    def upload_images(self, processed_bucket, image_media):
        for (size, image_format), upload_path in self.upload_paths.items():
            new_key = f"{image_media.filename}/{size}.{image_format}"
            content_type = "image/jpeg" if image_format == "jpg" else f"image/{image_format}"
            self.s3_client.upload_file(
                str(upload_path), processed_bucket, new_key, ExtraArgs={"ContentType": content_type}
            )
            upload_path.unlink(missing_ok=True)  # Clean up the temp file

    def process(self, image_media, processed_bucket):
        self.download_image(image_media)
        self.process_image(image_media)
        self.upload_images(processed_bucket, image_media)
        self.download_path.unlink(missing_ok=True)  # Clean up the original download


def lambda_handler(event, context):
    logger.info(event)

    s3_client = boto3.client("s3")
    processed_bucket = os.getenv("PROCESSED_MEDIA_BUCKET")

    processor = ImageProcessor(s3_client)
    for record in event["Records"]:
        raw_bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        image = ImageMedia(s3_client, raw_bucket, key)

        try:
            logger.info(f"Processing image {image.key}")
            processor.process(image, processed_bucket)
            logger.info(f"Processed image {image.key} successfully")
        except UnsupportedImageFormatError as e:
            logger.warning(f"Unsupported image format for {image.key}: {e}")
        except Exception as e:
            logger.error(f"Failed to process image {image.key}: {e}")

    return {"statusCode": 200, "body": "Image processed successfully"}
