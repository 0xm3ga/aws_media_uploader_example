import json
import logging
import os
from http import HTTPStatus

import boto3

from shared.media import Extension, Size
from shared.services.aws.api.api_base_service import ApiBaseService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_content_type(bucket_name, key):
    s3 = boto3.client("s3")
    response = s3.head_object(Bucket=bucket_name, Key=key)
    return response["ContentType"]


def get_filename(key):
    return key.split("/")[-1]


def lambda_handler(event, context):
    logger.info(event)

    lambda_client = boto3.client("lambda")
    image_processing_function_arn = os.environ.get("IMAGE_PROCESSING_FUNCTION_ARN")
    # video_processing_function_arn = os.environ.get("VIDEO_PROCESSING_FUNCTION_ARN")
    # gif_processing_function_arn = os.environ.get("GIF_PROCESSING_FUNCTION_ARN")

    # Record media metadata in RDS (TODO connect to actual RDS)
    try:
        metadata_function_arn = os.environ.get("RECORD_MEDIA_METADATA_FUNCTION_ARN")
        invoke_response = lambda_client.invoke(
            FunctionName=metadata_function_arn,
            InvocationType="Event",
            Payload=json.dumps(event),
        )
        logger.info(f"RecordMediaMetadataFunction invoked with response: {invoke_response}")
    except Exception:
        logger.error("RecordMediaMetadataFunction wasn't invoked")

    # Get bucket name and file key from the S3 event
    try:
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        logger.info(f"Processing file {key} from bucket {bucket}")
    except Exception:
        logger.error("Couldn't get bucket and key from the s3 record")
        return ApiBaseService.create_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message=json.dumps("Couldn't get bucket and key from the s3 record"),
        )

    # Getting additional info
    filename = get_filename(key)

    # Extract file extension
    content_type = get_content_type(bucket, key)
    logger.info(f"Content type: {content_type}")

    # Depending on the file type, dispatch to the appropriate Lambda function
    if content_type.startswith("image/"):
        # Specifying which format and what sizes to generate.
        extension = Extension.JPEG.name
        sizes = [
            Size.TINY.name,
            Size.SMALL.name,
            Size.MEDIUM.name,
            Size.LARGE.name,
            Size.HUGE.name,
        ]

        lambda_client.invoke(
            FunctionName=image_processing_function_arn,
            InvocationType="Event",
            Payload=json.dumps(
                {
                    "bucket": bucket,
                    "key": key,
                    "filename": filename,
                    "extension": extension,
                    "sizes": sizes,
                }
            ),
        )
    elif content_type.startswith("video/"):
        # TODO add vidoe processing lambda invokation
        # Video processing into mp4 lambda -> triggers image processing function
        # Thumbnail extraction lambda -> trigger image processing function
        # Git Extraction lambda
        pass

    else:
        logger.error(f"Unsupported content type: {content_type}")
        return ApiBaseService.create_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message=json.dumps(
                f"Unsupported content type: {content_type}",
            ),
        )

    return ApiBaseService.create_response(
        status_code=HTTPStatus.OK,
        message=json.dumps("Processing job started"),
    )
