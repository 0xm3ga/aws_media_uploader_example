class ApiMessages:
    class Error:
        JSON_SERIALIZATION_ERROR = "Failed to serialize JSON object: {error}"

    class Info:
        RESPONSE_CREATED = "Response created with status: {status}, message: {message}"
        REDIRECT_CREATED = "Redirect created with status: {status}, location: {location}"
