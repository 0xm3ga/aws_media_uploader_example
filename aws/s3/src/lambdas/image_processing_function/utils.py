import logging
import mimetypes
from typing import Any

from botocore.exceptions import BotoCoreError, ClientError
from enums import ALLOWED_IMAGE_EXTENSIONS, EXTENSION_MAP
from exceptions import S3AccessError, UnsupportedImageFormatError

# from enums import ImageFormat

# Logger setup
logger = logging.getLogger(__name__)


def get_content_type(s3_client: Any, bucket: str, key: str) -> str:
    """
    Get the content type of the file.

    :param s3_client: The S3 client
    :param bucket: The name of the S3 bucket
    :param key: The key of the file in the S3 bucket
    :return: Content type as a string.
    :raises S3AccessError: If there is an error accessing the S3 bucket.
    """
    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Failed to access S3 object with key {key} in bucket {bucket}: {e}")
        raise S3AccessError(bucket, key) from e

    if "ContentType" not in response:
        raise KeyError(f"No ContentType found for S3 object with key {key} in bucket {bucket}")

    return response["ContentType"]


def get_extension_from_content_type(content_type: str) -> str:
    """
    Get the file extension based on the content type.

    :param content_type: The content type of the file.
    :return: File extension as a string.
    :raises UnsupportedImageFormatError: If the content type is unknown or the extension is not
      supported.
    """
    assert isinstance(content_type, str), "content_type must be a string"

    extension = mimetypes.guess_extension(content_type)
    if extension is None:
        logger.warning(f"Unknown content type: {content_type}")
        raise UnsupportedImageFormatError(f"Unknown content type: {content_type}")

    extension = extension.lstrip(".")
    extension = EXTENSION_MAP.get(extension, extension)

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        logger.warning(f"Unsupported extension: {extension}")
        raise UnsupportedImageFormatError(f"Unsupported extension: {extension}")

    assert extension is not None, "extension should not be None at this point"

    return extension
