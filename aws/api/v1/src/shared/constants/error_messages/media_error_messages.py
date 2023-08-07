class MediaErrorMessages:
    INVALID_CONTENT_TYPE_FORMAT = (
        "Invalid content_type: {}. Should be in format 'media_type/extension'"
    )
    EMPTY_CONTENT_TYPE = "content_type cannot be empty"
    UNSUPPORTED_MEDIA_TYPE = "Unsupported media type: {media_type}"
    INVALID_CONTENT_TYPE = "Invalid content_type: {content_type}"
    EMPTY_EXTENSION = "extension cannot be empty"
    INVALID_EXTENSION = "Invalid extension: {extension}"
    # size related
    UNSUPPORTED_SIZE = "Unsupported size {size}"
    UNSUPPORTED_ASPECT_RATIO = "Unsupported aspect ratio {aspect_ratio}"
    UNSUPPORTED_MEDIA_TYPE = "Unsupported media type {media_type}"
    UNSUPPORTED_ASPECT_RATIO_FOR_MEDIA_TYPE = (
        "Unsupported aspect ratio {aspect_ratio} for media type {media_type}"
    )
    UNSUPPORTED_SIZE_FOR_ASPECT_RATIO = "Unsupported size {size} for aspect ratio {aspect_ratio}"
    INVALID_SIZE = "Invalid size provided."
    INVALID_ASPECT_RATIO = "Invalid aspect ratio provided."
    INVALID_MEDIA_TYPE = "Invalid media type provided."
