import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def download_file_from_s3(s3_client: Any, bucket: str, key: str, destination: Path) -> None:
    """
    Download a file from an S3 bucket

    :param s3_client: S3 client to handle file transfers
    :param bucket: Name of the S3 bucket
    :param key: Key of the file in the S3 bucket
    :param destination: Local path to save the downloaded file
    """
    try:
        s3_client.download_file(bucket, key, destination)
    except Exception as e:
        logger.error(f"Failed to download file from S3: {e}")
        raise


def upload_file_to_s3(
    s3_client: Any, file_path: str, bucket: str, key: str, content_type: str
) -> None:
    """
    Uploads a file to an S3 bucket

    :param s3_client: S3 client object
    :param file_path: Path to the file to upload
    :param bucket: The S3 bucket to upload to
    :param key: The S3 key (path within the bucket) at which to upload the file
    :param content_type: The content type of the file
    """
    try:
        print("bucket", bucket)
        print("key", key)
        print("file_path", file_path)
        s3_client.upload_file(file_path, bucket, key, ExtraArgs={"ContentType": content_type})
    except Exception as e:
        logger.error(f"Failed to upload file to S3: {e}")
        raise
