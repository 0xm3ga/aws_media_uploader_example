import logging
from http import HTTPStatus

import boto3
from botocore.exceptions import ClientError
from constants import error_messages as em
from exceptions import InvalidURLError

logger = logging.getLogger(__name__)


def object_exists(bucket: str, key: str) -> bool:
    """Check if an object exists in the S3 bucket."""
    try:
        s3_client = boto3.client("s3")
        s3_client.head_object(Bucket=bucket, Key=key)
        logger.info(em.OBJECT_FOUND_MSG.format(key=key, bucket=bucket))
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == HTTPStatus.NOT_FOUND:
            logger.warning(em.OBJECT_NOT_FOUND_MSG.format(key=key, bucket=bucket))
            return False
        else:
            logger.error(em.UNEXPECTED_ERROR_MSG.format(error_code=error_code, error=e))
            raise


def construct_processed_media_key(filename: str, size: str, extension: str) -> str:
    """Generate a key for processed media."""
    if not all([filename, size, extension]):
        logger.error(em.MISSING_OR_EMPTY_PARAM_MSG)
        raise ValueError(em.MISSING_OR_EMPTY_PARAM_MSG)

    if not all(isinstance(arg, str) for arg in [filename, size, extension]):
        logger.error(em.INVALID_PARAM_TYPE_MSG)
        raise TypeError(em.INVALID_PARAM_TYPE_MSG)

    processed_media_key = f"{filename}/{size}.{extension}"
    return processed_media_key


def construct_raw_media_key(filename: str, username: str, s3_prefix: str) -> str:
    """Generate a key for raw media file."""
    if not all([filename, username, s3_prefix]):
        logger.error(em.MISSING_OR_EMPTY_PARAM_MSG)
        raise ValueError(em.MISSING_OR_EMPTY_PARAM_MSG)

    if not all(isinstance(arg, str) for arg in [filename, username, s3_prefix]):
        logger.error(em.INVALID_PARAM_TYPE_MSG)
        raise TypeError(em.INVALID_PARAM_TYPE_MSG)

    raw_media_key = f"{username}/{s3_prefix}/{filename}"
    return raw_media_key


def construct_media_url(domain_name: str, path: str) -> str:
    """Generate a media URL with the provided domain name and path."""
    if not isinstance(domain_name, str) or not isinstance(path, str):
        logger.error(em.INVALID_URL_MSG)
        raise InvalidURLError

    return f"https://{domain_name}/{path}"
