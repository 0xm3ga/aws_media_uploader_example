import logging
from http import HTTPStatus

from shared.media.base import MediaFormatUtils
from shared.media.media_factory import MediaFactory
from shared.services.aws.api.api_base_service import ApiBaseService
from shared.services.aws.s3.s3_presigned_service import S3PresignService
from shared.services.environment_service import Environment
from shared.services.error_handler import error_handler
from shared.services.event_validation_service import EventValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@error_handler
def lambda_handler(event, context):
    """Lambda function handler."""

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
        HTTPStatus.OK,
        {
            "uploadURL": presigned_url,
            "filename": filename,
        },
    )
