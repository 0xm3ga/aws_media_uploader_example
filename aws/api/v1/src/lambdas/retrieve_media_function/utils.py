import json
import logging

import boto3
from botocore.exceptions import ClientError
from constants import ImageFormat, ImageSize
from exceptions import INVALID_URL_MSG, InvalidURLError, MediaProcessingError

logger = logging.getLogger(__name__)

lambda_client = boto3.client("lambda")
image_processing_function_arn = "aws-media-uploader-example-ImageProcessingFunction-vQK9O3NUU81c"


def generate_media_url(domain_name: str, path: str) -> str:
    """Generate a media URL with the provided domain name and path."""
    if not isinstance(domain_name, str) or not isinstance(path, str):
        logger.error(INVALID_URL_MSG)
        raise InvalidURLError

    return f"https://{domain_name}/{path}"


def object_exists(bucket: str, key: str) -> bool:
    """Check if an object exists in the S3 bucket."""
    logger.info(f"Checking if object {key} exists in bucket {bucket}...")

    try:
        s3_client = boto3.client("s3")
        s3_client.head_object(Bucket=bucket, Key=key)
        logger.info(f"Object {key} found in bucket {bucket}.")
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "404":
            logger.warning(f"Object {key} not found in bucket {bucket}.")
            return False
        else:
            logger.error(f"Unexpected error {error_code}: {e}")
            raise


def process_media(
    bucket: str,
    filename: str,
    size: str,
    extension: str,
    file_type: str,
    username: str,
) -> str:
    key = f"{username}/{file_type}/{filename}"

    if file_type == "images":
        try:
            format = ImageFormat[extension.upper()].name
            sizes = [ImageSize[size.upper()].name]
        except KeyError as e:
            logger.error(f"Invalid size or format provided: {e}")
            raise ValueError(f"Invalid size or format provided: {e}") from e

        logger.info("Invoking image processing lambda function")
        response = lambda_client.invoke(
            FunctionName=image_processing_function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {
                    "bucket": bucket,
                    "key": key,
                    "filename": filename,
                    "format": format,
                    "sizes": sizes,
                }
            ),
        )
        result = json.loads(response["Payload"].read())
        if "errorMessage" in result or "FunctionError" in response:
            logger.error(f"Error occurred during processing: {result}")
            raise MediaProcessingError(f"Error occurred during processing: {result}")

        logger.info(f"Image processing result: {result}")
    else:
        logger.error(f"File type {file_type} not supported. Cannot process.")
        raise MediaProcessingError(f"File type {file_type} not supported. Cannot process.")

    return f"{filename}/{size}.{extension}"
