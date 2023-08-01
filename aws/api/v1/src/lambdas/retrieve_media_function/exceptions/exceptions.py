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


class CustomException(Exception):
    """Base class for other exceptions"""

    def __init__(self, message, *args):
        self.message = message
        self.args = args
        super().__init__(message, *args)

    def __str__(self):
        return self.message


# Environment Variables
class EnvironmentVariableError(CustomException):
    """Exception raised for errors in the environment variables."""

    def __init__(self, var_name: str):
        self.var_name = var_name
        self.message = ENV_VAR_NOT_SET_MSG.format(var_name=self.var_name)
        super().__init__(self.var_name)


class MissingEnvironmentVariableError(CustomException):
    """Exception raised for missing environment variables."""

    def __init__(self, missing_vars: list):
        self.missing_vars = missing_vars
        self.message = MISSING_ENV_VARS_MSG.format(missing_vars=", ".join(missing_vars))
        super().__init__(self.missing_vars)


# RDS
class RDSCommunicationError(CustomException):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        super().__init__(error)
        self.message = RDS_COMMUNICATION_ERROR_MSG.format(error=error)


# Other
class PreprocessingError(CustomException):
    """Exception raised for preprocessing errors."""

    def __init__(self, message="An error occurred during preprocessing"):
        self.message = message
        super().__init__(message)


class UnsupportedExtensionError(PreprocessingError):
    """Exception raised when an unsupported file extension is encountered."""

    def __init__(self, extension: str):
        self.extension = extension
        super().__init__(UNSUPPORTED_EXTENSION_MSG.format(extension))


class UnsupportedSizeError(PreprocessingError):
    """Exception raised when an unsupported size is encountered."""

    def __init__(self, size: str):
        self.size = size
        super().__init__(UNSUPPORTED_SIZE_MSG.format(size))


class MissingRequiredRDSVariablesError(PreprocessingError):
    """Exception raised when required variables are missing in the response from RDS."""

    def __init__(self, missing_data: str):
        self.missing_data = missing_data
        self.message = INVALID_RDS_RESPONSE_MSG.format(missing_data=self.missing_data)
        super().__init__(self.message)


# Event validation
class MissingPathParamError(PreprocessingError):
    """Exception raised when a required path parameter is missing."""

    def __init__(self, param: str):
        self.param = param
        self.message = MISSING_PATH_PARAM_MSG.format(param=self.param)
        super().__init__(self.message)


class MissingQueryParamError(PreprocessingError):
    """Exception raised when a required query parameter is missing."""

    def __init__(self, param: str):
        self.param = param
        self.message = MISSING_QUERY_PARAM_MSG.format(param=self.param)
        super().__init__(self.message)


class InvalidParameterError(PreprocessingError):
    """Raised when a provided parameter is invalid."""

    def __init__(self, parameter_name):
        super().__init__(INVALID_PARAMETER_MSG.format(parameter_name))
        self.parameter_name = parameter_name


# Api Errors
class ObjectNotFoundError(CustomException):
    """Exception raised when an expected object is not found."""

    def __init__(self, message="Expected object was not found"):
        self.message = message
        super().__init__(message)


class InvalidURLError(TypeError):
    """Raised when unable to construct a URL due to invalid input types."""

    def __init__(self, message=INVALID_URL_MSG):
        self.message = message
        super().__init__(self.message)


# File processing
class FileProcessingError(CustomException):
    """Exception raised during file processing."""

    def __init__(self, message="An error occurred while processing the file"):
        self.message = message
        super().__init__(message)


class MediaProcessingError(Exception):
    """Raised when there is an error in media processing."""

    ERROR_INVOKING_LAMBDA = "Error occurred while invoking Lambda function: {}"
    ERROR_PROCESSING_RESPONSE = "Error occurred while processing Lambda function response: {}"
    ERROR_DURING_PROCESSING = "Error occurred during processing: {}"
    ERROR_UNSUPPORTED_FILE_TYPE = "File type {} not supported. Cannot process."

    def __init__(self, error_type, details=""):
        error_message = getattr(self, error_type, "").format(details)
        super().__init__(error_message)


class FeatureNotImplementedError(Exception):
    """Raised when a feature is not yet implemented."""

    ERROR_FEATURE_NOT_IMPLEMENTED = "The feature '{feature_name}' is not yet implemented."

    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        self.message = self.ERROR_FEATURE_NOT_IMPLEMENTED.format(feature_name=feature_name)
        super().__init__(self.feature_name)
