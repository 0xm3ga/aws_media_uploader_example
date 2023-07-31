import logging
import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def object_exists(bucket: str, key: str):
    logger.info(f"object_exists: {bucket} {key}")
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise
    else:
        return True


def process_media(filename: str, size: str, extension: str) -> str:
    username = "username"
    file_type = "videos"

    key = f"{username}/{file_type}/{size}"
    return key


def lambda_handler(event, context):
    logger.info(event)
    try:
        raw_media_bucket = os.environ["RAW_MEDIA_BUCKET"]
        processed_media_bucket = os.environ["PROCESSED_MEDIA_BUCKET"]
        media_domain_name = os.environ["MEDIA_DOMAIN_NAME"]

        filename = event["pathParameters"]["filename"]  # fetch filename from the url path parameter

        queryStringParameters = event.get("queryStringParameters") or {}
        size = queryStringParameters.get("size", "medium")
        extension = queryStringParameters.get("extension", "jpeg")

        # Make sure to use jpeg instead of jpg
        if extension == "jpg":
            extension = "jpeg"

        # List of accepted sizes
        accepted_sizes = ["tiny", "small", "medium", "large", "huge"]

        # List of accepted formats
        accepted_formats = ["jpg", "jpeg", "png", "gif", "mp4"]

        if size not in accepted_sizes:
            size = "medium"

        # Check if the provided format is in the list of accepted formats
        if extension not in accepted_formats:
            return {"statusCode": 400, "body": f"Extension {extension} is not supported."}

    except Exception as e:
        logger.error(f"Preprocessing error: {str(e)}")
        return {"statusCode": 500, "body": f"Preprocessing error: {str(e)}"}

    try:
        # Construct the key
        key = f"{filename}/{size}.{extension}"
        logger.info(key)

        # Check that the object exists in processed bucket
        if not object_exists(processed_media_bucket, key):
            logger.info(f"Object {key} not found in processed bucket. Checking raw bucket...")
            # Check that the original object exists in raw bucket
            if not object_exists(raw_media_bucket, key):
                logger.warning(f"Object {key} not found in raw bucket.")
                return {"statusCode": 404, "body": f"Object not found: {str(key)}"}

            # TODO: call processing lambda (for just the specified size and ext)
            try:
                key = process_media(filename, size, extension)
            except Exception:
                logger.error("Error processing the file.")
                return {"statusCode": 500, "body": "Error processing the file."}

        url = f"https://{media_domain_name}/{key}"

        return {
            "statusCode": 302,
            "headers": {
                "Location": url,
            },
        }

    except NoCredentialsError:
        logger.error("No AWS credentials found")
        return {"statusCode": 403, "body": "No AWS credentials found"}
    except Exception as e:
        logger.error(str(e))
        return {"statusCode": 500, "body": str(e)}
