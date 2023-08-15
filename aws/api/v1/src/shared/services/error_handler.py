import json
import logging
from functools import wraps
from http import HTTPStatus

from shared.exceptions import AppError

logger = logging.getLogger(__name__)


def error_handler(func):
    """Decorator to handle errors and return appropriate responses."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            # Return the error response
            return e.to_dict()
        except Exception as e:
            # Handle other exceptions and return a generic error response
            logger.error(f"Unhandled error occurred: {str(e)}")
            return {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": json.dumps({"message": "Internal Server Error"}),
            }

    return wrapper
