import logging
from http import HTTPStatus

import exceptions as ex
from botocore.exceptions import NoCredentialsError
from constants import error_messages as em
from custom_types import RetrieveMediaEvent
from media_request import MediaRequest
from utils.environment_utils import Environment
from utils.s3_utils import construct_media_url
from validation import fetch_parameters_from_event

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event: RetrieveMediaEvent, context):
    """Lambda function handler."""
    try:
        logger.info("Fetching environment variables.")

        # env vars
        env = Environment(["RAW_MEDIA_BUCKET", "MEDIA_DOMAIN_NAME"])
        env.fetch_required_variables()

        raw_media_bucket = env.fetch_variable("RAW_MEDIA_BUCKET")
        media_domain_name = env.fetch_variable("MEDIA_DOMAIN_NAME")

        # fetch and validate params from event
        logger.info("Fetching parameters from event.")
        filename, size, extension = fetch_parameters_from_event(event)

        # processing request
        logger.info("Processing media request.")
        media_request = MediaRequest(filename, size, extension, raw_media_bucket)
        key = media_request.process()

        # construct response
        logger.info("Constructing response.")
        url = construct_media_url(media_domain_name, key)
        return {"statusCode": HTTPStatus.FOUND, "headers": {"Location": url}}

    except NoCredentialsError as e:
        logger.error(em.NO_AWS_CREDENTIALS_MSG.format(str(e)))
        return {"statusCode": HTTPStatus.FORBIDDEN, "body": em.NO_AWS_CREDENTIALS_MSG}
    except ex.PreprocessingError as e:
        logger.error(em.PREPROCESSING_ERROR_MSG.format(str(e)))
        return {"statusCode": HTTPStatus.BAD_REQUEST, "body": str(e)}
    except ex.ObjectNotFoundError as e:
        logger.error(em.OBJECT_NOT_FOUND_MSG.format(str(e)))
        return {"statusCode": HTTPStatus.NOT_FOUND, "body": str(e)}
    except ex.FileProcessingError as e:
        logger.error(em.FILE_PROCESSING_ERROR_MSG.format(str(e)))
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": em.FILE_PROCESSING_ERROR_MSG,
        }
    except Exception as e:
        logger.error(em.INTERNAL_SERVER_ERROR_MSG.format(str(e)))
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "body": str(e)}
