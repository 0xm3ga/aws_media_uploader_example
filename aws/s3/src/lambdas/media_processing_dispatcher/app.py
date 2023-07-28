import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)


def get_content_type(bucket_name, key):
    s3 = boto3.client("s3")
    response = s3.head_object(Bucket=bucket_name, Key=key)
    return response["ContentType"]


def lambda_handler(event, context):
    logger.info(event)

    lambda_client = boto3.client("lambda")

    # Trigger the RecordMediaMetadataFunction
    metadata_function_arn = os.environ.get("RECORD_MEDIA_METADATA_FUNCTION_ARN")
    invoke_response = lambda_client.invoke(
        FunctionName=metadata_function_arn,
        InvocationType="Event",
        Payload=json.dumps(event),
    )

    # Log Lambda invocation response
    logger.info(f"RecordMediaMetadataFunction invoked with response: {invoke_response}")

    # Get bucket name and file key from the S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    # Log bucket and key information
    logger.info(f"Processing file {key} from bucket {bucket}")

    # Extract file extension
    content_type = get_content_type(bucket, key)

    # Log content type
    logger.info(f"Content type: {content_type}")

    # Depending on the file type, dispatch to the appropriate Lambda function
    if content_type.startswith("image/"):
        function_arn = os.environ.get("IMAGE_PROCESSING_FUNCTION_ARN")
    elif content_type.startswith("video/"):
        function_arn = os.environ.get("VIDEO_PROCESSING_FUNCTION_ARN")
    else:
        logger.error(f"Unsupported content type: {content_type}")
        return

    # Trigger the respective Lambda function
    invoke_response = lambda_client.invoke(
        FunctionName=function_arn,
        InvocationType="Event",
        Payload=json.dumps(event),
    )

    # Log Lambda invocation response
    logger.info(f"Lambda function invoked with response: {invoke_response}")

    return {"statusCode": 200, "body": json.dumps("Processing job started")}
