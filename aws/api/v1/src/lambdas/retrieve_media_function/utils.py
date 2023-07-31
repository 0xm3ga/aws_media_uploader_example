import json
import logging
from typing import List, Tuple

import boto3
from botocore.exceptions import ClientError
from constants import FileType, ImageFormat, ImageSize
from exceptions import (
    INVALID_URL_MSG,
    FeatureNotImplementedError,
    InvalidURLError,
    MediaProcessingError,
)

logger = logging.getLogger(__name__)

lambda_client = boto3.client("lambda")
image_processing_function_arn = "aws-media-uploader-example-ImageProcessingFunction-vQK9O3NUU81c"


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


def object_exists(bucket: str, key: str) -> bool:
    """Check if an object exists in the S3 bucket."""
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


def invoke_image_processing_lambda_function(
    bucket: str, key: str, filename: str, image_format: str, sizes: List[str]
) -> dict:
    """Invokes the image processing Lambda function and returns its response."""
    payload = {
        "bucket": bucket,
        "key": key,
        "filename": filename,
        "format": image_format,
        "sizes": sizes,
    }

    try:
        logger.info(f"Invoking image processing lambda function with payload: {payload}")
        response = lambda_client.invoke(
            FunctionName=image_processing_function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )
        if response["StatusCode"] != 200:
            raise Exception(f"Unexpected status code: {response['StatusCode']}")
    except Exception as e:
        logger.error(MediaProcessingError.ERROR_INVOKING_LAMBDA, str(e))
        raise MediaProcessingError(MediaProcessingError.ERROR_INVOKING_LAMBDA, str(e))

    return response


def process_lambda_response(response: dict) -> dict:
    """Processes the response from the Lambda function and returns the result."""
    try:
        result = json.loads(response["Payload"].read())
        if "errorMessage" in result or "FunctionError" in response:
            logger.error(MediaProcessingError.ERROR_DURING_PROCESSING, result)
            raise MediaProcessingError(MediaProcessingError.ERROR_DURING_PROCESSING, result)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(MediaProcessingError.ERROR_PROCESSING_RESPONSE, str(e))
        raise MediaProcessingError(MediaProcessingError.ERROR_PROCESSING_RESPONSE, str(e))

    return result


def validate_image_properties(size: str, extension: str) -> Tuple[List[str], str]:
    """Validates and returns the image size and format."""
    try:
        sizes = [ImageSize[size.upper()].name]
    except KeyError as e:
        logger.error(f"Invalid size provided: {e}")
        raise ValueError(f"Invalid size provided: {e}") from e

    try:
        image_format = ImageFormat[extension.upper()].name
    except KeyError as e:
        logger.error(f"Invalid format provided: {e}")
        raise ValueError(f"Invalid format provided: {e}") from e

    return sizes, image_format


def process_media(
    bucket: str, filename: str, size: str, extension: str, file_type: str, username: str
) -> str:
    """Processes the media based on its type and returns the key of the processed media."""
    key = construct_raw_media_key(filename, username, file_type)

    sizes, image_format = validate_image_properties(size, extension)

    if file_type == FileType.IMAGE.value:
        response = invoke_image_processing_lambda_function(
            bucket,
            key,
            filename,
            image_format,
            sizes,
        )
        result = process_lambda_response(response)
        logger.info(result)

    elif file_type == FileType.VIDEO.value:
        feature_name = "Video processing"
        logger.error(FeatureNotImplementedError.ERROR_FEATURE_NOT_IMPLEMENTED, feature_name)
        raise FeatureNotImplementedError(feature_name)

    else:
        logger.error(MediaProcessingError.ERROR_UNSUPPORTED_FILE_TYPE, file_type)
        raise MediaProcessingError(MediaProcessingError.ERROR_UNSUPPORTED_FILE_TYPE, file_type)

    return construct_processed_media_key(filename, size, extension)
