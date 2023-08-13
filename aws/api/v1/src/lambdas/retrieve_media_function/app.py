import logging
from http import HTTPStatus

from shared.constants.log_messages import LambdaLogMessages
from shared.media.base import MediaFormatUtils, MediaSizeUtils
from shared.services.aws.api.api_base_service import ApiBaseService
from shared.services.environment_service import Environment
from shared.services.event_validation_service import EventValidator

from .error_handler import handle_exception
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


def lambda_handler(event, context):
    """Main AWS Lambda handler for retrieving media."""
    logger.info(
        LambdaLogMessages.LAMBDA_INVOKED.format(request_id=context.aws_request_id, event=event)
    )

    try:
        # Fetch and set the necessary environment variables for media processing
        env = Environment(["PROCESSED_MEDIA_BUCKET", "RAW_MEDIA_BUCKET", "MEDIA_DOMAIN_NAME"])
        env.fetch_required_variables()

        processed_media_bucket = env.fetch_variable("PROCESSED_MEDIA_BUCKET")
        raw_media_bucket = env.fetch_variable("RAW_MEDIA_BUCKET")
        media_domain_name = env.fetch_variable("MEDIA_DOMAIN_NAME")

        # Extract and validate necessary event parameters
        filename, size, extension = extract_and_validate_event(event)

        # Process the media request and retrieve the processed media URL
        media_request = MediaRequest(processed_media_bucket, raw_media_bucket, media_domain_name)
        url = media_request.process(filename, size, extension)
        return ApiBaseService.create_redirect(HTTPStatus.FOUND, url)

    except Exception as e:
        # Handle and log exceptions, then return appropriate error response
        status, message = handle_exception(e, logger)
        return ApiBaseService.create_response(status, message)

    finally:
        # Log the completion of the Lambda invocation
        logger.info(LambdaLogMessages.LAMBDA_COMPLETED.format(request_id=context.aws_request_id))
