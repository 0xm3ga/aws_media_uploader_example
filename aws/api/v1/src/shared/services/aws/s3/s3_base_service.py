import logging
from http import HTTPStatus

import boto3
from botocore.exceptions import ClientError
from shared.constants.logging_messages import S3Messages

logger = logging.getLogger(__name__)


class S3BaseService:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def object_exists(self, bucket: str, key: str) -> bool:
        """Check if an object exists in the S3 bucket."""
        try:
            self.s3_client.head_object(Bucket=bucket, Key=key)
            logger.info(S3Messages.Info.OBJECT_FOUND.format(key=key, bucket=bucket))
            return True
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == HTTPStatus.NOT_FOUND:
                logger.warning(S3Messages.Error.OBJECT_NOT_FOUND.format(key=key, bucket=bucket))
                return False
            else:
                logger.error(
                    S3Messages.Error.UNEXPECTED_ERROR.format(
                        error_code=error_code,
                        error=str(e),
                    )
                )
                raise

    @staticmethod
    def construct_processed_media_key(filename: str, size: str, extension: str) -> str:
        """Generate a key for processed media."""
        if not all([filename, size, extension]):
            logger.error(S3Messages.Error.MISSING_OR_EMPTY_PARAM)
            raise ValueError(S3Messages.Error.MISSING_OR_EMPTY_PARAM)

        if not all(isinstance(arg, str) for arg in [filename, size, extension]):
            logger.error(S3Messages.Error.INVALID_PARAM_TYPE)
            raise TypeError(S3Messages.Error.INVALID_PARAM_TYPE)

        processed_media_key = f"{filename}/{size}.{extension}"
        return processed_media_key

    @staticmethod
    def construct_raw_media_key(filename: str, username: str, s3_prefix: str) -> str:
        """Generate a key for raw media file."""
        if not all([filename, username, s3_prefix]):
            logger.error(S3Messages.Error.MISSING_OR_EMPTY_PARAM)
            raise ValueError(S3Messages.Error.MISSING_OR_EMPTY_PARAM)

        if not all(isinstance(arg, str) for arg in [filename, username, s3_prefix]):
            logger.error(S3Messages.Error.INVALID_PARAM_TYPE)
            raise TypeError(S3Messages.Error.INVALID_PARAM_TYPE)

        raw_media_key = f"{username}/{s3_prefix}/{filename}"
        logger.info(S3Messages.Info.GENERATED_S3_KEY.format(key=raw_media_key, username=username))
        return raw_media_key

    @staticmethod
    def construct_media_url(domain_name: str, path: str) -> str:
        """Generate a media URL with the provided domain name and path."""
        if not isinstance(domain_name, str) or not isinstance(path, str):
            logger.error(S3Messages.Error.INVALID_URL)
            raise ValueError(S3Messages.Error.INVALID_URL)

        return f"https://{domain_name}/{path}"
