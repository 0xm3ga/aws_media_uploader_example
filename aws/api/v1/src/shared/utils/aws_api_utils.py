import json
from http import HTTPStatus
from typing import Any


def create_response(status_code: HTTPStatus, message: Any):
    return {
        "statusCode": status_code,
        "body": json.dumps(message),
    }


def create_redirect(status_code: HTTPStatus, location: str):
    """
    Creates a standard HTTP redirect response.
    """
    return {
        "statusCode": status_code,
        "headers": {"Location": location},
    }
