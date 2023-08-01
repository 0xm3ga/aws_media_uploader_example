ENV_VAR_NOT_SET_MSG = "Environment variable {var_name} not set."
MISSING_ENV_VARS_MSG = "Missing required environment variable(s): {missing_vars}"

# RDS
RDS_COMMUNICATION_ERROR_MSG = "Error communicating with RDS: {error}"
INVALID_RDS_RESPONSE_MSG = "Invalid RDS response, missing required variables: {missing_data}"

# Processing
UNSUPPORTED_EXTENSION_MSG = "Extension {extension} is not supported."
UNSUPPORTED_SIZE_MSG = "Size '{size}' is not supported."

NO_PATH_PARAMS_MSG = "No path parameters provided in the event."
NO_QUERY_PARAMS_MSG = "No query parameters provided in the event."
MISSING_PATH_PARAM_MSG = "Path parameter {param} is missing from the event."
MISSING_QUERY_PARAM_MSG = "Query parameter {param} is missing from the event."

INVALID_PARAMETER_MSG = "{} is invalid."
INVALID_URL_MSG = "Invalid input type. Couldn't construct URL."

# valdiation
INVALID_FORMAT_MSG = "Invalid format provided: {extension}."
INVALID_SIZE_MSG = "Invalid size provided: {size}."
MISSING_OR_EMPTY_PARAM_MSG = "One or more parameters are missing or empty."
INVALID_PARAM_TYPE_MSG = "One or more parameters are not of type string."

# S3
OBJECT_FOUND_MSG = "Object {key} found in bucket {bucket}."
OBJECT_NOT_FOUND_MSG = "Object {key} not found in bucket {bucket}."
UNEXPECTED_ERROR_MSG = "Unexpected error {error_code}: {error}"

# AWS
NO_AWS_CREDENTIALS_MSG = "No AWS credentials found"

# HTTP
BAD_REQUEST_MSG = "PreprocessingError occurred: {}"
OBJECT_NOT_FOUND_MSG = "ObjectNotFoundError occurred: {}"
FILE_PROCESSING_ERROR_MSG = "FileProcessingError occurred: {}"
UNEXPECTED_ERROR_MSG = "Unexpected error occurred: {}"
PREPROCESSING_ERROR_MSG = "Preprocessing error occurred: {}"
INTERNAL_SERVER_ERROR_MSG = "Internal server error occurred: {}"

# Lambda
ERROR_INVOKING_LAMBDA_MSG = "Error occurred while invoking Lambda function: {}"
ERROR_PROCESSING_RESPONSE_MSG = "Error occurred while processing Lambda function response: {}"
ERROR_DURING_PROCESSING_MSG = "Error occurred during processing: {}"
ERROR_UNSUPPORTED_FILE_TYPE_MSG = "File type {} not supported. Cannot process."

# Features
FEATURE_NOT_IMPLEMENTED_ERROR_MSG = "The feature '{feature_name}' is not yet implemented."
