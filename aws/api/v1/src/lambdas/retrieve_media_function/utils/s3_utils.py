import logging
from http import HTTPStatus

import boto3
from botocore.exceptions import ClientError
from constants.error_messages import INVALID_URL_MSG
from exceptions import InvalidURLError

logger = logging.getLogger(__name__)


def object_exists(bucket: str, key: str) -> bool:
    """Check if an object exists in the S3 bucket."""
    try:
        s3_client = boto3.client("s3")
        s3_client.head_object(Bucket=bucket, Key=key)
        logger.info(f"Object {key} found in bucket {bucket}.")
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == HTTPStatus.NOT_FOUND:
            logger.warning(f"Object {key} not found in bucket {bucket}.")
            return False
        else:
            logger.error(f"Unexpected error {error_code}: {e}")
            raise


def construct_processed_media_key(filename: str, size: str, extension: str) -> str:
    """Generate a key for processed media."""

    # Check if any argument is missing
    if not all([filename, size, extension]):
        logger.error("One or more parameters are missing or empty.")
        raise ValueError("All parameters should be non-empty.")

    # Check if all arguments are of type 'str'
    if not all(isinstance(arg, str) for arg in [filename, size, extension]):
        logger.error("One or more parameters are not of type string.")
        raise TypeError("All parameters should be of type string.")

    processed_media_key = f"{filename}/{size}.{extension}"
    return processed_media_key


def construct_raw_media_key(filename: str, username: str, file_type: str) -> str:
    """Generate a key for raw media file."""

    # Check if any argument is missing
    if not all([filename, username, file_type]):
        logger.error("One or more parameters are missing or empty.")
        raise ValueError("All parameters should be non-empty.")

    # Check if all arguments are of type 'str'
    if not all(isinstance(arg, str) for arg in [filename, username, file_type]):
        logger.error("One or more parameters are not of type string.")
        raise TypeError("All parameters should be of type string.")

    raw_media_key = f"{username}/{file_type}/{filename}"
    return raw_media_key


def construct_media_url(domain_name: str, path: str) -> str:
    """Generate a media URL with the provided domain name and path."""
    if not isinstance(domain_name, str) or not isinstance(path, str):
        logger.error(INVALID_URL_MSG)
        raise InvalidURLError

    return f"https://{domain_name}/{path}"
