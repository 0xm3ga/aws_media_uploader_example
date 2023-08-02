import logging
from http import HTTPStatus

import shared.exceptions as ex
from botocore.exceptions import NoCredentialsError
from shared.constants import error_messages as em
from shared.services.aws_s3_presigned_service import S3PresignService
from shared.services.environment_service import Environment
from shared.services.event_validation_service import EventValidator
from shared.utils.aws_api_utils import create_response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


allowed_content_type = [
    "image/jpeg",
    "image/png",
    "video/mp4",
    "image/mov",
]


def lambda_handler(event, context):
    """Lambda function handler."""
    try:
        # env vars
        logger.info("Fetching environment variables.")
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
            allowed_values=allowed_content_type,
        )

        # generating presigned url
        s3_presign_service = S3PresignService()
        filename, presigned_url = s3_presign_service.generate_presigned_url(
            content_type=content_type,
            username=username,
            raw_bucket_name=raw_bucket_name,
        )

        return create_response(HTTPStatus.OK, {"uploadURL": presigned_url, "filename": filename})

    except NoCredentialsError as e:
        logger.error(em.NO_AWS_CREDENTIALS_MSG.format(str(e)))
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, em.NO_AWS_CREDENTIALS_MSG)

    except (ex.MissingParameterError, ex.InvalidTypeError, ex.InvalidValueError) as e:
        return create_response(HTTPStatus.BAD_REQUEST, str(e))

    except ex.UnauthorizedError:
        logger.error(em.UNAUTHORIZED_ERROR_MSG)
        return create_response(HTTPStatus.UNAUTHORIZED, em.UNAUTHORIZED_ERROR_MSG)

    except Exception:
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, em.INTERNAL_SERVER_ERROR_MSG)


lambda_handler({}, {})
