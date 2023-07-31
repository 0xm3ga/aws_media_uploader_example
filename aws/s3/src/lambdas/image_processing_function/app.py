import logging
import os
from http import HTTPStatus

import boto3
from aws_image_service import AWSImageProcessingService
from enums import ImageFormat, ImageSize
from exceptions import EnvironmentVariableNotFound, ValidationError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_event(event):
    """
    Validate the event object for required keys
    :param event: dict
    :return: Tuple[str, str, str, str, list]
    """
    bucket = event.get("bucket")
    key = event.get("key")
    filename = event.get("filename")
    format = event.get("format")
    sizes = event.get("sizes")

    ValidationError.check_required_fields(event, ["bucket", "key", "filename", "format", "sizes"])
    ValidationError.check_value(format, ImageFormat._member_names_, "format")
    ValidationError.check_subset(sizes, ImageSize._member_names_, "sizes")
    ValidationError.check_non_empty_list(sizes, "sizes")

    return bucket, key, filename, ImageFormat[format], [ImageSize[size] for size in sizes]


def lambda_handler(event, context):
    logger.info(event)

    processed_bucket = os.getenv("PROCESSED_MEDIA_BUCKET", "media.bluecollarverse.com-processed")
    if processed_bucket is None:
        logger.error(EnvironmentVariableNotFound.ENV_ERROR_MSG.format("PROCESSED_MEDIA_BUCKET"))
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "body": "Internal Server Error"}

    try:
        bucket, key, filename, format, sizes = validate_event(event)
    except ValidationError as e:
        logger.error("Validation Error: %s", e)
        return {"statusCode": HTTPStatus.BAD_REQUEST, "body": str(e)}

    s3_client = boto3.client("s3")
    service = AWSImageProcessingService(s3_client, processed_bucket)

    try:
        service.process_image(bucket, key, filename, format, sizes)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "body": "Internal Server Error"}

    return {"statusCode": HTTPStatus.OK, "body": "Images are being processed."}
