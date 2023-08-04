import logging
from http import HTTPStatus

import shared.exceptions as ex
from botocore.exceptions import NoCredentialsError
from models.media_request import MediaRequest
from shared.constants.error_messages import (
    AwsErrorMessages,
    HttpErrorMessages,
    ProcessingErrorMessages,
    S3ErrorMessages,
)
from shared.constants.media_constants.media import MediaFormat, MediaSize
from shared.services.aws.api.api_base_service import ApiBaseService
from shared.services.environment_service import Environment
from shared.services.event_validation_service import EventValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def extract_and_validate_event(event):
    """Extracts parameters from the event and validates them."""
    validator = EventValidator(event)
    filename = validator.get_path_parameter(
        "filename",
        optional=False,
        expected_type=str,
    )

    size = validator.get_query_string_parameter(
        "size",
        optional=False,
        expected_type=str,
        allowed_values=MediaSize.allowed_sizes(),
    )

    extension = validator.get_query_string_parameter(
        "extension",
        optional=False,
        expected_type=str,
        allowed_values=MediaFormat.allowed_extensions(),
    )

    return filename, size, extension


def lambda_handler(event, context):
    """Lambda function handler."""
    try:
        # env vars
        logger.info("Fetching environment variables.")
        env = Environment(["PROCESSED_MEDIA_BUCKET", "RAW_MEDIA_BUCKET", "MEDIA_DOMAIN_NAME"])
        env.fetch_required_variables()

        processed_media_bucket = env.fetch_variable("PROCESSED_MEDIA_BUCKET")
        raw_media_bucket = env.fetch_variable("RAW_MEDIA_BUCKET")
        media_domain_name = env.fetch_variable("MEDIA_DOMAIN_NAME")

        # fetch and validate params from event
        logger.info("Processing event.")
        filename, size, extension = extract_and_validate_event(event)

        # processing request
        logger.info("Processing media request.")
        media_request = MediaRequest(processed_media_bucket, raw_media_bucket, media_domain_name)
        url = media_request.process(filename, size, extension)
        return ApiBaseService.create_redirect(HTTPStatus.FOUND, url)

    except NoCredentialsError as e:
        logger.error(AwsErrorMessages.NO_AWS_CREDENTIALS.format(str(e)))
        return ApiBaseService.create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, HttpErrorMessages.INTERNAL_SERVER_ERROR
        )

    except (
        ex.PreprocessingError,
        ex.MissingParameterError,
        ex.InvalidTypeError,
        ex.InvalidValueError,
    ) as e:
        logger.error(ProcessingErrorMessages.GENERIC_PROCESSING_ERROR.format(str(e)))
        return ApiBaseService.create_response(HTTPStatus.BAD_REQUEST, str(e))

    except ex.ObjectNotFoundError as e:
        logger.error(S3ErrorMessages.OBJECT_NOT_FOUND.format(str(e)))
        return ApiBaseService.create_response(HTTPStatus.NOT_FOUND, str(e))

    except ex.FileProcessingError as e:
        logger.error(ProcessingErrorMessages.GENERIC_PROCESSING_ERROR.format(str(e)))
        return ApiBaseService.create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, HttpErrorMessages.INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        logger.error(HttpErrorMessages.INTERNAL_SERVER_ERROR.format(str(e)))
        return ApiBaseService.create_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
