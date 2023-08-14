class HttpMessages:
    class Error:
        BAD_REQUEST = "PreprocessingError occurred: {}"
        OBJECT_NOT_FOUND = "ObjectNotFoundError occurred: {}"
        FILE_PROCESSING_ERROR = "FileProcessingError occurred: {}"
        UNEXPECTED_ERROR = "Unexpected error occurred: {error}"
        PREPROCESSING_ERROR = "Preprocessing error occurred: {error}"
        FORBIDDEN = "Forbidden: access denied."
        RESOURCE_NOT_FOUND = "Resource not found."
        UNEXPECTED_STATUS_CODE = "Unexpected status code: {status_code}"
        UNAUTHORIZED = "Unauthorized."
        INTERNAL_SERVER_ERROR = "Internal server error."

    class Info:
        pass  # Placeholder for HTTP related info messages
