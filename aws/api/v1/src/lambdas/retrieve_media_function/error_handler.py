# error_handler.py

from http import HTTPStatus

from botocore.exceptions import NoCredentialsError
from shared.constants.error_messages import (
    AwsErrorMessages,
    HttpErrorMessages,
    ProcessingErrorMessages,
)
from shared.exceptions import (
    FileProcessingError,
    InvalidTypeError,
    InvalidValueError,
    MissingParameterError,
    ObjectNotFoundError,
    PreprocessingError,
    S3ErrorMessages,
)

EXCEPTION_MAPPING = {
    NoCredentialsError: {
        "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        "message": AwsErrorMessages.NO_AWS_CREDENTIALS,
        "log": True,
    },
    PreprocessingError: {
        "status": HTTPStatus.BAD_REQUEST,
        "message": ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
        "log": True,
    },
    MissingParameterError: {
        "status": HTTPStatus.BAD_REQUEST,
        "message": ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
        "log": True,
    },
    InvalidTypeError: {
        "status": HTTPStatus.BAD_REQUEST,
        "message": ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
        "log": True,
    },
    InvalidValueError: {
        "status": HTTPStatus.BAD_REQUEST,
        "message": ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
        "log": True,
    },
    ObjectNotFoundError: {
        "status": HTTPStatus.NOT_FOUND,
        "message": S3ErrorMessages.OBJECT_NOT_FOUND,
        "log": True,
    },
    FileProcessingError: {
        "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        "message": HttpErrorMessages.INTERNAL_SERVER_ERROR,
        "log": True,
    },
}


def handle_exception(e, logger):
    exception_data = EXCEPTION_MAPPING.get(type(e), None)
    if exception_data:
        message = exception_data["message"].format(str(e))
        if exception_data.get("log"):
            logger.error(message)
        return exception_data["status"], message
    else:
        # Generic fallback
        logger.error(HttpErrorMessages.INTERNAL_SERVER_ERROR.format(str(e)))
        return HTTPStatus.INTERNAL_SERVER_ERROR, str(e)
