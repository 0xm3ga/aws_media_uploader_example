from typing import Tuple

from shared.constants import error_messages as em
from shared.constants.media_constants.base_media import MediaType
from shared.exceptions import MediaProcessingError


def parse_content_type(content_type: str) -> Tuple[str, str]:
    try:
        primary_type, extension = content_type.split("/")
    except ValueError:
        raise MediaProcessingError(em.INVALID_CONTENT_TYPE.format(content_type))

    return primary_type, extension


def convert_content_type_to_file_type(content_type: str) -> str:
    """Converts a MIME type to a corresponding media type."""

    primary_type, _ = parse_content_type(content_type)
    try:
        return MediaType(primary_type).s3_prefix
    except Exception:
        raise MediaProcessingError(em.UNSUPPORTED_MIME_TYPE_ERROR_MSG.format(content_type))
