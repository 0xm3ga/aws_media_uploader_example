import json
import logging
from typing import List

from shared.constants.logging_messages import LambdaMessages
from shared.exceptions import MediaProcessingError
from shared.media.constants import Extension, Size
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
        extension: Extension,
        sizes: List[Size],
    ) -> dict:
        """Creates the payload for the Lambda function invocation."""
        return {
            "bucket": bucket,
            "key": key,
            "filename": filename,
            "extension": extension.value,
            "sizes": [size.name for size in sizes],
        }

    def invoke_lambda_function(
        self,
        bucket: str,
        key: str,
        filename: str,
        extension: Extension,
        sizes: List[Size],
    ) -> dict:
        """Invokes the image processing Lambda function and returns its response."""
        payload = self._create_payload(bucket, key, filename, extension, sizes)
        response = self.lambda_invoker.invoke(self.function_arn, payload)
        processed_response = self._extract_and_process_response(response)
        return processed_response

    def _extract_payload_from_response(self, response: dict):
        try:
            return json.loads(response["Payload"].read())
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(LambdaMessages.Error.ERROR_PROCESSING_RESPONSE.format(error=str(e)))
            raise MediaProcessingError(
                LambdaMessages.Error.ERROR_PROCESSING_RESPONSE.format(error=str(e))
            )

    def _check_response_for_errors(self, response: dict):
        if "errorMessage" in response or "FunctionError" in response:
            logger.error(LambdaMessages.Error.ERROR_DURING_PROCESSING.format(error=response))
            raise MediaProcessingError(
                LambdaMessages.Error.ERROR_DURING_PROCESSING.format(error=response)
            )

    def _extract_and_process_response(self, response: dict) -> dict:
        """Extracts payload from response and checks for any errors."""
        payload = self._extract_payload_from_response(response)
        self._check_response_for_errors(payload)

        return payload
