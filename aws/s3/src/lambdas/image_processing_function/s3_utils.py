import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def download_file_from_s3(s3_client: Any, bucket: str, key: str, destination: Path) -> None:
    """
    Download a file from an S3 bucket
    """
    try:
        s3_client.download_file(bucket, key, destination)
    except Exception as e:
        logger.error(f"Failed to download file from S3: {e}")
        raise


def upload_file_to_s3(
    s3_client: Any, file_path: Path, bucket: str, key: str, content_type: str
) -> None:
    """
    Uploads a file to an S3 bucket
    """
    try:
        s3_client.upload_file(file_path, bucket, key, ExtraArgs={"ContentType": content_type})
    except Exception as e:
        logger.error(f"Failed to upload file to S3: {e}")
        raise
