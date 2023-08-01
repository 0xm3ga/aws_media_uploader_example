import json
import logging
from typing import List

import boto3
from constants import error_messages as em
from exceptions import MediaProcessingError

logger = logging.getLogger(__name__)


lambda_client = boto3.client("lambda")
image_processing_function_arn = "aws-media-uploader-example-ImageProcessingFunction-vQK9O3NUU81c"


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
        logger.error(em.ERROR_INVOKING_LAMBDA_MSG, str(e))
        raise MediaProcessingError(em.ERROR_INVOKING_LAMBDA_MSG, str(e))

    return response


def process_lambda_response(response: dict) -> dict:
    """Processes the response from the Lambda function and returns the result."""
    try:
        result = json.loads(response["Payload"].read())
        if "errorMessage" in result or "FunctionError" in response:
            logger.error(em.ERROR_DURING_PROCESSING_MSG, result)
            raise MediaProcessingError(em.ERROR_DURING_PROCESSING_MSG, result)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(em.ERROR_PROCESSING_RESPONSE_MSG, str(e))
        raise MediaProcessingError(em.ERROR_PROCESSING_RESPONSE_MSG, str(e))

    return result
