from http import HTTPStatus

from botocore.exceptions import NoCredentialsError
from custom_types import RetrieveMediaEvent
from environment import Environment
from exceptions import FileProcessingError, ObjectNotFoundError, PreprocessingError
from media_request import MediaRequest
from utils import construct_media_url
from validation import fetch_parameters_from_event


def lambda_handler(event: RetrieveMediaEvent, context):
    """Lambda function handler."""
    try:
        # env vars
        env = Environment(["RAW_MEDIA_BUCKET", "MEDIA_DOMAIN_NAME"])
        env.fetch_required_variables()

        raw_media_bucket = env.fetch_variable("RAW_MEDIA_BUCKET")
        media_domain_name = env.fetch_variable("MEDIA_DOMAIN_NAME")

        # fetch and validate params from event
        filename, size, extension = fetch_parameters_from_event(event)

        # processing request
        media_request = MediaRequest(filename, size, extension, raw_media_bucket)
        key = media_request.process()

        # construct response
        url = construct_media_url(media_domain_name, key)
        return {"statusCode": HTTPStatus.FOUND, "headers": {"Location": url}}

    except NoCredentialsError:
        return {"statusCode": HTTPStatus.FORBIDDEN, "body": "No AWS credentials found"}
    except PreprocessingError as e:
        return {"statusCode": HTTPStatus.BAD_REQUEST, "body": str(e)}
    except ObjectNotFoundError as e:
        return {"statusCode": HTTPStatus.NOT_FOUND, "body": str(e)}
    except FileProcessingError:
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": "Error processing the file.",
        }
    except Exception as e:
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "body": str(e)}
