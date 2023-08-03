class HttpErrorMessages:
    BAD_REQUEST = "PreprocessingError occurred: {}"
    OBJECT_NOT_FOUND = "ObjectNotFoundError occurred: {}"
    FILE_PROCESSING_ERROR = "FileProcessingError occurred: {}"
    UNEXPECTED_ERROR = "Unexpected error occurred: {error}"
    PREPROCESSING_ERROR = "Preprocessing error occurred: {error}"

    # Error messages for HTTP status codes
    FORBIDDEN = "Forbidden: access denied."
    RESOURCE_NOT_FOUND = "Resource not found."
    UNEXPECTED_STATUS_CODE = "Unexpected status code: {status_code}"
    UNAUTHORIZED = "Unauthorized."
    INTERNAL_SERVER_ERROR = "Internal server error."
