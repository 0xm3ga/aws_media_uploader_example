import logging

from constants.file_types import FileType
from exceptions import FeatureNotImplementedError, MediaProcessingError
from utils.aws_services import invoke_image_processing_lambda_function, process_lambda_response
from utils.image_processing import validate_image_properties
from utils.s3_utils import construct_processed_media_key, construct_raw_media_key

logger = logging.getLogger(__name__)


def process_media(
    bucket: str, filename: str, size: str, extension: str, file_type: str, username: str
) -> str:
    """Processes the media based on its type and returns the key of the processed media."""
    key = construct_raw_media_key(filename, username, file_type)

    sizes, image_format = validate_image_properties(size, extension)

    if file_type == FileType.IMAGE.value:
        response = invoke_image_processing_lambda_function(
            bucket,
            key,
            filename,
            image_format,
            sizes,
        )
        result = process_lambda_response(response)
        logger.info(result)

    elif file_type == FileType.VIDEO.value:
        feature_name = "Video processing"
        logger.error(FeatureNotImplementedError.ERROR_FEATURE_NOT_IMPLEMENTED, feature_name)
        raise FeatureNotImplementedError(feature_name)

    else:
        logger.error(MediaProcessingError.ERROR_UNSUPPORTED_FILE_TYPE, file_type)
        raise MediaProcessingError(MediaProcessingError.ERROR_UNSUPPORTED_FILE_TYPE, file_type)

    return construct_processed_media_key(filename, size, extension)
