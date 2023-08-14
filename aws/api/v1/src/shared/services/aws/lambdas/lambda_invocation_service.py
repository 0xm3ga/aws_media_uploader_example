import json
import logging
from http import HTTPStatus

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from shared.constants.logging_messages import HttpMessages, LambdaMessages
from shared.exceptions import MediaProcessingError

logger = logging.getLogger(__name__)


class LambdaInvoker:
    """A class to invoke AWS Lambda functions."""

    def __init__(self):
        self.lambda_client = boto3.client("lambda")

    def invoke(self, function_arn: str, payload: dict) -> dict:
        """Invokes a Lambda function and returns its response."""
        logger.info(
            "Invoking lambda function",
            extra={
                "function_arn": function_arn,
                "payload": payload,
            },
        )

        try:
            response = self.lambda_client.invoke(
                FunctionName=function_arn,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )
        except (BotoCoreError, ClientError) as e:
            logger.error(LambdaMessages.Error.ERROR_INVOKING_LAMBDA.format(str(e)))
            raise MediaProcessingError(LambdaMessages.Error.ERROR_INVOKING_LAMBDA.format(str(e)))

        return self._process_response(response)

    def _process_response(self, response: dict) -> dict:
        if response["StatusCode"] != HTTPStatus.OK:
            if response["StatusCode"] == HTTPStatus.FORBIDDEN:
                raise MediaProcessingError(HttpMessages.Error.FORBIDDEN)
            elif response["StatusCode"] == HTTPStatus.NOT_FOUND:
                raise MediaProcessingError(HttpMessages.Error.RESOURCE_NOT_FOUND)
            else:
                raise MediaProcessingError(
                    HttpMessages.Error.UNEXPECTED_STATUS_CODE.format(
                        status_code=response["StatusCode"]
                    )
                )
        return response
