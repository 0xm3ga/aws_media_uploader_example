import json
import logging
from typing import List

from shared.constants.error_messages import LambdaErrorMessages
from shared.constants.media_constants import ImageFormat, ImageSize
from shared.exceptions import MediaProcessingError
from shared.services.aws.lambdas.lambda_invocation_service import LambdaInvoker

logger = logging.getLogger(__name__)

# TODO: ref env var
ARN = "arn:aws:lambda:us-east-1:149501512243:function:aws-media-uploader-example-\
    ImageProcessingFunction-vQK9O3NUU81c"


class ImageProcessingInvoker:
    """A class to invoke the image processing Lambda function."""

    def __init__(self):
        self.lambda_invoker = LambdaInvoker()
        self.function_arn = ARN

    def _create_payload(
        self,
        bucket: str,
        key: str,
        filename: str,
        format: ImageFormat,
        sizes: List[ImageSize],
    ) -> dict:
        """Creates the payload for the Lambda function invocation."""
        return {
            "bucket": bucket,
            "key": key,
            "filename": filename,
            "format": format.value,
            "sizes": [size.name for size in sizes],
        }

    def invoke_lambda_function(
        self,
        bucket: str,
        key: str,
        filename: str,
        format: ImageFormat,
        sizes: List[ImageSize],
    ) -> dict:
        """Invokes the image processing Lambda function and returns its response."""
        payload = self._create_payload(bucket, key, filename, format, sizes)
        response = self.lambda_invoker.invoke(self.function_arn, payload)
        processed_response = self._extract_and_process_response(response)
        return processed_response

    def _extract_payload_from_response(self, response: dict):
        try:
            return json.loads(response["Payload"].read())
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(LambdaErrorMessages.ERROR_PROCESSING_RESPONSE.format(str(e)))
            raise MediaProcessingError(LambdaErrorMessages.ERROR_PROCESSING_RESPONSE.format(str(e)))

    def _check_response_for_errors(self, response: dict):
        if "errorMessage" in response or "FunctionError" in response:
            logger.error(LambdaErrorMessages.ERROR_DURING_PROCESSING.format(response))
            raise MediaProcessingError(LambdaErrorMessages.ERROR_DURING_PROCESSING.format(response))

    def _extract_and_process_response(self, response: dict) -> dict:
        """Extracts payload from response and checks for any errors."""
        payload = self._extract_payload_from_response(response)
        self._check_response_for_errors(payload)

        return payload
