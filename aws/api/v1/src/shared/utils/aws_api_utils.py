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

    Args:
        status_code (HTTPStatus): The HTTP status code of the response.
        location (str): The redirect location URL.

    Returns:
        Dict[str, Optional[Union[int, str]]]: The constructed HTTP response.
    """
    return {"statusCode": status_code, "headers": {"Location": location}}
