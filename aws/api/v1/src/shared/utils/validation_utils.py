import logging

import exceptions as ex
from constants import error_messages as em
from constants.media_constants.media import MediaFormat, MediaSize

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def normalize_extension(extension: str) -> str:
    """Normalize the extension."""
    logger.info("Normalizing the extension.")

    try:
        extension_normalized = str(extension).strip().lower()
    except Exception as e:
        logger.error(f"Error while normalizing extension: {e}")
        raise ex.InvalidParameterError(str(e))

    return "jpeg" if extension_normalized == "jpg" else extension_normalized


def validate_size(size: str) -> str:
    """Validate the requested size."""
    logger.info("Validating size")

    try:
        size = str(size).strip().lower()
    except Exception as e:
        logger.error(em.INVALID_PARAMETER_MSG.format(str(e)))
        raise ex.InvalidParameterError(str(e))

    if size not in MediaSize.allowed_sizes():
        logger.error(em.UNSUPPORTED_SIZE_MSG.format(size))
        raise ex.UnsupportedSizeError(size)

    return size


def validate_extension(extension: str) -> str:
    """Validate the requested extension."""
    logger.info("Validating extension")

    try:
        extension = str(extension).strip().lower()
    except Exception as e:
        logger.error(em.INVALID_PARAMETER_MSG.format(str(e)))
        raise ex.InvalidParameterError(str(e))

    extension_normalized = normalize_extension(extension)
    if extension_normalized not in MediaFormat.allowed_extensions():
        logger.error(em.UNSUPPORTED_EXTENSION_MSG.format(extension_normalized))
        raise ex.UnsupportedExtensionError(extension_normalized)

    return extension_normalized


def fetch_parameters_from_event(event):
    """Fetch parameters from the event data."""
    logger.info("Fetching parameters from event")

    path_parameters = event.get("pathParameters")
    if path_parameters is None:
        logger.error(em.NO_PATH_PARAMS_MSG)
        raise ex.MissingPathParamError(em.NO_PATH_PARAMS_MSG)

    try:
        filename = path_parameters["filename"]
    except KeyError:
        logger.error(em.MISSING_PATH_PARAM_MSG.format("filename"))
        raise ex.MissingPathParamError("filename")

    query_parameters = event.get("queryStringParameters")
    if query_parameters is None:
        logger.error(em.NO_QUERY_PARAMS_MSG)
        raise ex.MissingQueryParamError(em.NO_QUERY_PARAMS_MSG)

    try:
        size = query_parameters["size"]
        extension = query_parameters["extension"]
    except KeyError as e:
        logger.error(em.MISSING_QUERY_PARAM_MSG.format(str(e)))
        raise ex.MissingQueryParamError(str(e))

    # Validate size and extension before returning them
    size = validate_size(size)
    extension = validate_extension(extension)

    return filename, size, extension
