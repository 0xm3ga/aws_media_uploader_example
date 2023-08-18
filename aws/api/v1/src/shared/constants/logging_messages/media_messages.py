class MediaMessages:
    class Error:
        GENERIC_ERROR = "Generic media error"
        INVALID_MEDIA_TYPE = "Invalid media type provided."
        INVALID_CONTENT_TYPE = "Invalid content_type: {content_type}"
        INVALID_SIZE = "Invalid size provided."
        INVALID_ASPECT_RATIO = "Invalid aspect ratio provided."
        INVALID_EXTENSION = "Invalid extension: {extension}"

        EMPTY_CONTENT_TYPE = "content_type cannot be empty"

        UNSUPPORTED_EXTENSION = "Extension {extension} is not supported."
        UNSUPPORTED_SIZE = "Size '{size}' is not supported."
        UNSUPPORTED_MEDIA_TYPE = "Unsupported media type: {media_type}"
        UNSUPPORTED_SIZE = "Unsupported size {size}"
        UNSUPPORTED_ASPECT_RATIO = "Unsupported aspect ratio {aspect_ratio}"
        UNSUPPORTED_ASPECT_RATIO_FOR_MEDIA_TYPE = (
            "Unsupported aspect ratio {aspect_ratio} for media type {media_type}"
        )
        UNSUPPORTED_SIZE_FOR_ASPECT_RATIO = (
            "Unsupported size {size} for aspect ratio {aspect_ratio}"
        )

    class Info:
        pass

    class User:
        UNSUPPORTED_MEDIA_TYPE = "Unsupported media type: {media_type}"
