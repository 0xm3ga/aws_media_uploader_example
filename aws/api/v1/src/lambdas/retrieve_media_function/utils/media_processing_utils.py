from constants import error_messages as em
from exceptions import MediaProcessingError


def convert_content_type_to_file_type(content_type: str) -> str:
    """Converts a MIME type to a corresponding media type."""

    primary_type, subtype = content_type.split("/")

    if primary_type == "image":
        return "images"
    elif primary_type == "video":
        return "videos"
    else:
        raise MediaProcessingError(em.UNSUPPORTED_MIME_TYPE_ERROR_MSG.format(content_type))
