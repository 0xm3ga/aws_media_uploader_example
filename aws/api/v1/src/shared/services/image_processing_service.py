import json
import logging
from typing import List

from constants import error_messages as em
from exceptions import MediaProcessingError
from services.lambda_invocation_service import LambdaInvoker

logger = logging.getLogger(__name__)

# TODO: ref env var
arn = "arn:aws:lambda:us-east-1:149501512243:function:aws-media-uploader-example-\
    ImageProcessingFunction-vQK9O3NUU81c"


class ImageProcessingInvoker:
    """A class to invoke the image processing Lambda function."""

    def __init__(self):
        self.lambda_invoker = LambdaInvoker()
        self.function_arn = arn

    def _create_payload(
        self, bucket: str, key: str, filename: str, format: str, sizes: List[str]
    ) -> dict:
        """Creates the payload for the Lambda function invocation."""
        return {
            "bucket": bucket,
            "key": key,
            "filename": filename,
            "format": format,
            "sizes": sizes,
        }

    def invoke_lambda_function(
        self, bucket: str, key: str, filename: str, format: str, sizes: List[str]
    ) -> dict:
        """Invokes the image processing Lambda function and returns its response."""
        payload = self._create_payload(bucket, key, filename, format, sizes)
        response = self.lambda_invoker.invoke(self.function_arn, payload)
        processed_response = self.extract_and_process_response(response)
        return processed_response

    def _extract_payload_from_response(self, response: dict):
        try:
            return json.loads(response["Payload"].read())
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(em.ERROR_PROCESSING_RESPONSE_MSG.format(str(e)))
            raise MediaProcessingError(em.ERROR_PROCESSING_RESPONSE_MSG.format(str(e)))

    def _check_response_for_errors(self, response: dict):
        if "errorMessage" in response or "FunctionError" in response:
            logger.error(em.ERROR_DURING_PROCESSING_MSG.format(response))
            raise MediaProcessingError(em.ERROR_DURING_PROCESSING_MSG.format(response))

    def extract_and_process_response(self, response: dict) -> dict:
        """Extracts payload from response and checks for any errors."""
        payload = self._extract_payload_from_response(response)
        self._check_response_for_errors(payload)

        return payload
