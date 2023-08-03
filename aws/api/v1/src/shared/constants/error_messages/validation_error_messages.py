class ValidationErrorMessages:
    INVALID_FORMAT = "Invalid format provided: {extension}."
    INVALID_SIZE = "Invalid size provided: {size}."
    MISSING_OR_EMPTY_PARAM = "One or more parameters are missing or empty."
    INVALID_PARAM_TYPE = "One or more parameters are not of type string."
    UNSUPPORTED_MIME_TYPE = "Unsupported MIME type: {}"

    MISSING_PARAMETER = "The '{parameter}' parameter is missing from the event."
    INVALID_TYPE = (
        "The '{parameter}' parameter is of type '{actual}', but expected type was '{expected}'."
    )
    PARAMETER_NOT_IN_SET = "The '{parameter}' parameter has a value of '{value}', which is \
            not in the set of allowed values: {allowed_values}."

    UNAUTHORIZED = "Unauthorized access"
