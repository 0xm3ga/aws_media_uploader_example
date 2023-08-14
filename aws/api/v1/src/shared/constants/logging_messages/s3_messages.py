class S3Messages:
    class Error:
        OBJECT_NOT_FOUND = "Object {key} not found in bucket: {bucket}"
        UNEXPECTED_ERROR = "Unexpected error {error_code}. Error: {error}"
        MISSING_OR_EMPTY_PARAM = "Missing or empty parameter"
        INVALID_PARAM_TYPE = "Invalid parameter type"
        INVALID_URL = "Invalid URL"
        PRE_SIGNED_URL_GENERATION_FAILED = "Presigned URL generation failed: {error}"
        FAILED_TO_GENERATE_PRESIGNED_URL = "An error occurred generating the presigned URL: {error}"

    class Info:
        OBJECT_FOUND = "Object found: {key} in bucket: {bucket}"
        GENERATED_S3_KEY = "Generated S3 key: {key} for user: {username}"
        GENERATED_PRESIGNED_URL = "Generated presigned URL for filename: {filename}"
