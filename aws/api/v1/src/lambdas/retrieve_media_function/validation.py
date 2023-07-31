import logging

from constants import ACCEPTED_FORMATS, ACCEPTED_SIZES
from custom_types import RetrieveMediaEvent
from exceptions import (
    INVALID_PARAMETER_MSG,
    MISSING_PATH_PARAM_MSG,
    MISSING_QUERY_PARAM_MSG,
    NO_PATH_PARAMS_MSG,
    NO_QUERY_PARAMS_MSG,
    UNSUPPORTED_EXTENSION_MSG,
    UNSUPPORTED_SIZE_MSG,
    InvalidParameterError,
    MissingPathParamError,
    MissingQueryParamError,
    UnsupportedExtensionError,
    UnsupportedSizeError,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def normalize_extension(extension: str) -> str:
    """Normalize the extension."""
    try:
        extension_normalized = str(extension).strip().lower()
    except Exception as e:
        logger.error(f"Error while normalizing extension: {e}")
        raise InvalidParameterError(str(e))

    return "jpeg" if extension_normalized == "jpg" else extension_normalized


def validate_size(size: str) -> str:
    """Validate the requested size."""
    logger.info("Validating size")

    try:
        size = str(size).strip().lower()
    except Exception as e:
        logger.error(INVALID_PARAMETER_MSG.format(str(e)))
        raise InvalidParameterError(str(e))

    if size not in ACCEPTED_SIZES:
        logger.error(UNSUPPORTED_SIZE_MSG.format(size))
        raise UnsupportedSizeError(size)

    return size


def validate_extension(extension: str) -> str:
    """Validate the requested extension."""
    logger.info("Validating extension")

    try:
        extension = str(extension).strip().lower()
    except Exception as e:
        logger.error(INVALID_PARAMETER_MSG.format(str(e)))
        raise InvalidParameterError(str(e))

    extension_normalized = normalize_extension(extension)
    if extension_normalized not in ACCEPTED_FORMATS:
        logger.error(UNSUPPORTED_EXTENSION_MSG.format(extension_normalized))
        raise UnsupportedExtensionError(extension_normalized)

    return extension_normalized


def fetch_parameters_from_event(event: RetrieveMediaEvent):
    """Fetch parameters from the event data."""
    logger.info("Fetching parameters from event")

    path_parameters = event.get("pathParameters")
    if path_parameters is None:
        logger.error(NO_PATH_PARAMS_MSG)
        raise MissingPathParamError(NO_PATH_PARAMS_MSG)

    try:
        filename = path_parameters["filename"]
    except KeyError:
        logger.error(MISSING_PATH_PARAM_MSG.format("filename"))
        raise MissingPathParamError("filename")

    query_parameters = event.get("queryStringParameters")
    if query_parameters is None:
        logger.error(NO_QUERY_PARAMS_MSG)
        raise MissingQueryParamError(NO_QUERY_PARAMS_MSG)

    try:
        size = query_parameters["size"]
        extension = query_parameters["extension"]
    except KeyError as e:
        logger.error(MISSING_QUERY_PARAM_MSG.format(str(e)))
        raise MissingQueryParamError(str(e))

    # Validate size and extension before returning them
    size = validate_size(size)
    extension = validate_extension(extension)

    return filename, size, extension
