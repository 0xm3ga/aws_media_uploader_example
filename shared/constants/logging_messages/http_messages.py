class HttpMessages:
    class Error:
        UNEXPECTED_ERROR = "Unexpected error occurred: {error}"
        FORBIDDEN = "Forbidden: access denied."
        RESOURCE_NOT_FOUND = "Resource not found."
        UNEXPECTED_STATUS_CODE = "Unexpected status code: {status_code}"
        UNAUTHORIZED = "Unauthorized."
        INTERNAL_SERVER_ERROR = "Internal server error."

    class Info:
        pass

    class User:
        INTERNAL_SERVER_ERROR = "Internal server error."
        BAD_REQUEST = "Bad request"
        OBJECT_NOT_FOUND = "Object not found."
        UNAUTHORIZED = "Unauthorized."
