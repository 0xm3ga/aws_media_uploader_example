import logging
from http import HTTPStatus

from shared.constants.error_messages import HttpErrorMessages
from shared.exceptions import (
    InvalidContentTypeError,
    InvalidTypeError,
    InvalidValueError,
    MissingParameterError,
    UnauthorizedError,
)
from shared.media.base import MediaFormatUtils
from shared.media.media_factory import MediaFactory
from shared.services.aws.api.api_base_service import ApiBaseService
from shared.services.aws.s3.s3_presigned_service import S3PresignService
from shared.services.environment_service import Environment
from shared.services.event_validation_service import EventValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Lambda function handler."""
    try:
        # env vars
        env = Environment(["RAW_MEDIA_BUCKET"])
        env.fetch_required_variables()

        raw_bucket_name = env.fetch_variable("RAW_MEDIA_BUCKET")

        # getting vars from event
        validator = EventValidator(event)
        username = validator.get_authorizer_parameter("username")
        content_type = validator.get_query_string_parameter(
            "content_type",
            optional=False,
            expected_type=str,
            allowed_values=MediaFormatUtils.allowed_content_types(),
        )

        media = MediaFactory().create_media_from_content_type(content_type)

        # generating presigned url
        s3_presign_service = S3PresignService()
        filename, presigned_url = s3_presign_service.generate_presigned_url(
            media=media,
            username=username,
            raw_bucket_name=raw_bucket_name,
        )

        return ApiBaseService.create_response(
            HTTPStatus.OK, {"uploadURL": presigned_url, "filename": filename}
        )

    except (
        MissingParameterError,
        InvalidTypeError,
        InvalidValueError,
        InvalidContentTypeError,
    ) as e:
        logger.error(HttpErrorMessages.UNEXPECTED_ERROR.format(error=str(e)))
        return ApiBaseService.create_response(HTTPStatus.BAD_REQUEST, str(e))

    except UnauthorizedError:
        logger.error(HttpErrorMessages.UNAUTHORIZED)
        return ApiBaseService.create_response(
            HTTPStatus.UNAUTHORIZED, HttpErrorMessages.UNAUTHORIZED
        )

    except Exception as e:
        logger.error(HttpErrorMessages.UNEXPECTED_ERROR.format(error=str(e)))
        return ApiBaseService.create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, HttpErrorMessages.INTERNAL_SERVER_ERROR
        )
