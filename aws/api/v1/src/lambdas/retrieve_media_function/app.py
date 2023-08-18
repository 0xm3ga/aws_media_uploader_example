import logging
from http import HTTPStatus

from shared.constants.logging_messages import LambdaMessages
from shared.media.base import MediaFormatUtils, MediaSizeUtils
from shared.services.aws.api.api_base_service import ApiBaseService
from shared.services.environment_service import Environment
from shared.services.error_handler import error_handler
from shared.services.event_validation_service import EventValidator

from .models.media_request import MediaRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def extract_and_validate_event(event):
    """Extract and validate necessary parameters from the provided event."""
    validator = EventValidator(event)

    # Extract filename from the path parameters
    filename = validator.get_path_parameter(
        "filename",
        optional=False,
        expected_type=str,
    )

    # Extract size and extension from the query string parameters
    size = validator.get_query_string_parameter(
        "size",
        optional=False,
        expected_type=str,
        allowed_values=MediaSizeUtils.allowed_sizes(),
    )

    extension = validator.get_query_string_parameter(
        "extension",
        optional=False,
        expected_type=str,
        allowed_values=MediaFormatUtils.allowed_extensions(),
    )

    return filename, size, extension


@error_handler
def lambda_handler(event, context):
    """Main AWS Lambda handler for retrieving media."""
    logger.info(
        LambdaMessages.Info.LAMBDA_INVOKED.format(
            request_id=context.get("aws_request_id", ""),
            event=event,
        )
    )

    # Fetch and set the necessary environment variables for media processing
    env = Environment(["PROCESSED_MEDIA_BUCKET", "RAW_MEDIA_BUCKET", "MEDIA_DOMAIN_NAME"])
    processed_media_bucket = env.fetch_variable("PROCESSED_MEDIA_BUCKET")
    raw_media_bucket = env.fetch_variable("RAW_MEDIA_BUCKET")
    media_domain_name = env.fetch_variable("MEDIA_DOMAIN_NAME")

    # Extract and validate necessary event parameters
    filename, size, extension = extract_and_validate_event(event)

    # Process the media request and retrieve the processed media URL
    media_request = MediaRequest(processed_media_bucket, raw_media_bucket, media_domain_name)
    url = media_request.process(filename, size, extension)

    # Log the completion of the Lambda invocation
    logger.info(
        LambdaMessages.Info.LAMBDA_COMPLETED.format(
            request_id=context.get("aws_request_id", ""),
        )
    )
    return ApiBaseService.create_redirect(HTTPStatus.FOUND, url)
