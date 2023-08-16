class ValidationMessages:
    class Error:
        GENERIC_ERROR = "Generic event validation error"

        MISSING_PARAM = "Missing '{param}' parameter from the event."
        MISSING_AUTHORIZER = "Missing '{authorizer}' authorizer from the event."
        MISSING_PATH_PARAM = "Missing '{param}' path param from the event."
        MISSING_QUERY_STR_PARAM = "Missing '{param}' query string param in the event."

        INVALID_PARAM = "Invalid '{param}' parameter in the the event."
        INVALID_PARAM_TYPE = "The '{param}' parameter is of type '{actual}', \
            but expected type is '{allowed}'."
        INVALID_PARAM_VALUE = "The '{param}' parameter has a value of '{actual}', \
            which is not in the set of allowed values: {allowed}."

        # === TO DO: review
        INVALID_FORMAT = "Invalid format provided: {extension}."
        INVALID_SIZE = "Invalid size provided: {size}."
        UNSUPPORTED_MIME_TYPE = "Unsupported MIME type: {mimetype}"
        MISSING_OR_EMPTY_PARAM = "One or more parameters are missing or empty."

    class Info:
        VALIDATION_SUCCESSFUL = "Validation successful for {parameter}"
        AUTHORIZE_SUCCESSFUL = "Successfully authorized parameter: {parameter}"

    class User:
        MISSING_PARAM = "'{param}' parameter is required."
        MISSING_PATH_PARAM = "'{param}' path param is required."
        MISSING_QUERY_STR_PARAM = "'{param}' query string param is required."

        INVALID_PARAM = "Invalid '{param}' parameter."
        INVALID_PARAM_TYPE = "'{param}' parameter type is not allowed."
        INVALID_PARAM_VALUE = "'{param}' parameter value of '{actual}', \
            in not allowed. Allowed values: {allowed}."
