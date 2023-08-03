class ProcessingErrorMessages:
    GENERIC_PROCESSING_ERROR = "An error occurred during preprocessing"

    UNSUPPORTED_EXTENSION = "Extension {extension} is not supported."
    UNSUPPORTED_SIZE = "Size '{size}' is not supported."

    NO_PATH_PARAMS = "No path parameters provided in the event."
    NO_QUERY_PARAMS = "No query parameters provided in the event."
    MISSING_PATH_PARAM = "Path parameter {param} is missing from the event."
    MISSING_QUERY_PARAM = "Query parameter {param} is missing from the event."

    INVALID_PARAMETER = "{} is invalid."
    INVALID_URL = "Invalid input type. Couldn't construct URL."

    MISSING_FIELD_IN_RESPONSE_ERROR = "Expected field '{}' is missing in the response."
    NULL_OR_EMPTY_FIELD_IN_RESPONSE_ERROR = "Field '{}' in the response is null or empty."

    INVALID_CONTENT_TYPE = "Invalid content type received: {}"
