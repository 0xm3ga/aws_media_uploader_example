import base64
import binascii
import json
import logging
import os
from mimetypes import guess_extension
from urllib.parse import urljoin
from uuid import uuid4

import boto3
from botocore.exceptions import NoCredentialsError


class InvalidInputError(Exception):
    """Exception raised for invalid input errors."""

    pass


class InvalidFileTypeError(Exception):
    """Exception raised for invalid file type."""

    pass


s3 = boto3.client("s3")

MEDIA_BUCKET_NAME = os.getenv("MEDIA_BUCKET_NAME")
if not MEDIA_BUCKET_NAME:
    raise ValueError("The MEDIA_BUCKET_NAME environment variable is not set.")

ALLOWED_EXTENSIONS = {".png", ".jpg", ".mp4"}

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class S3Uploader:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def _get_s3_file_url(self, filename):
        """Construct and return the URL of a file in an S3 bucket."""
        return urljoin(f"https://{self.bucket_name}.s3.amazonaws.com", filename)

    def upload_file(self, filename, file_content):
        """Upload a file to an S3 bucket."""
        try:
            self.s3.put_object(
                Bucket=self.bucket_name, Key=filename, Body=file_content, ACL="public-read"
            )
            url = self._get_s3_file_url(filename)
            logger.info(f"File uploaded successfully at {url}")
            return url
        except NoCredentialsError:
            logger.error("No AWS credentials found.")
            raise
        except Exception as e:
            logger.error(f"An error occurred while uploading the file: {e}")
            raise


def make_response(status_code, message, data=None):
    """Create a standardized API response."""
    response = {
        "statusCode": status_code,
        "body": json.dumps({"message": message, "data": data}),
    }
    return response


def validate_file_type(file_extension):
    """Validate file type."""
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}")


def generate_filename(file_extension):
    """Generate a unique filename based on a UUID."""
    return f"{uuid4()}{file_extension}"


def lambda_handler(event, context):
    try:
        # Validate and decode the input
        try:
            base64_string = event["body"]
            file_extension = guess_extension(event["headers"].get("content-type"))
            decoded_file = base64.b64decode(base64_string)
        except KeyError as e:
            raise InvalidInputError(f"Invalid input: {e}")
        except (TypeError, binascii.Error) as e:
            raise InvalidInputError(f"Invalid base64 input: {e}")

        # Validate the file type
        validate_file_type(file_extension)

        # Generate a filename and upload the file to S3
        filename = generate_filename(file_extension)
        uploader = S3Uploader(MEDIA_BUCKET_NAME)
        url = uploader.upload_file(filename, decoded_file)

        # Return a successful response
        return make_response(200, "File uploaded successfully.", {"url": url, "filename": filename})

    except InvalidInputError as e:
        return make_response(400, str(e))
    except InvalidFileTypeError as e:
        return make_response(400, str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred during processing: {e}", exc_info=True)
        return make_response(500, "An error occurred during processing.")
