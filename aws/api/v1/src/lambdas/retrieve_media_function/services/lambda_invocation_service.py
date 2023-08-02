import json
import logging
from http import HTTPStatus

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from constants import error_messages as em
from exceptions import MediaProcessingError

logger = logging.getLogger(__name__)


class LambdaInvoker:
    """A class to invoke AWS Lambda functions."""

    def __init__(self):
        self.lambda_client = boto3.client("lambda")

    def invoke(self, function_arn: str, payload: dict) -> dict:
        """Invokes a Lambda function and returns its response."""
        logger.info(
            "Invoking lambda function", extra={"function_arn": function_arn, "payload": payload}
        )

        try:
            response = self.lambda_client.invoke(
                FunctionName=function_arn,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )
        except (BotoCoreError, ClientError) as e:
            logger.error(em.ERROR_INVOKING_LAMBDA_MSG.format(str(e)))
            raise MediaProcessingError(em.ERROR_INVOKING_LAMBDA_MSG.format(str(e)))

        return self._process_response(response)

    def _process_response(self, response: dict) -> dict:
        if response["StatusCode"] != HTTPStatus.OK:
            if response["StatusCode"] == HTTPStatus.FORBIDDEN:
                raise MediaProcessingError(em.FORBIDDEN_ERROR_MSG)
            elif response["StatusCode"] == HTTPStatus.NOT_FOUND:
                raise MediaProcessingError(em.RESOURCE_NOT_FOUND_ERROR_MSG)
            else:
                raise MediaProcessingError(
                    em.UNEXPECTED_STATUS_CODE_ERROR_MSG.format(response["StatusCode"])
                )
        return response
