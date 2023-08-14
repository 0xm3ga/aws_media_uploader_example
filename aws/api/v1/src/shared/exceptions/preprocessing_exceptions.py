from shared.constants.logging_messages import GeneralMessages, ProcessingMessages, RdsMessages

from .base_exceptions import CustomException


class PreprocessingError(CustomException):
    """Exception raised for preprocessing errors."""

    def __init__(self, message=GeneralMessages.Error.UNEXPECTED_ERROR):
        self.message = message
        super().__init__(message)


class UnsupportedExtensionError(PreprocessingError):
    """Exception raised when an unsupported file extension is encountered."""

    def __init__(self, extension: str):
        self.extension = extension
        super().__init__(ProcessingMessages.Error.UNSUPPORTED_EXTENSION.format(extension))


class UnsupportedSizeError(PreprocessingError):
    """Exception raised when an unsupported size is encountered."""

    def __init__(self, size: str):
        self.size = size
        super().__init__(ProcessingMessages.Error.UNSUPPORTED_SIZE.format(size))


class MissingRequiredRDSVariablesError(PreprocessingError):
    """Exception raised when required variables are missing in the response from RDS."""

    def __init__(self, missing_data: str):
        self.missing_data = missing_data
        self.message = RdsMessages.Error.INVALID_RDS_RESPONSE.format(missing_data=self.missing_data)
        super().__init__(self.message)


class MissingPathParamError(PreprocessingError):
    """Exception raised when a required path parameter is missing."""

    def __init__(self, param: str):
        self.param = param
        self.message = ProcessingMessages.Error.MISSING_PATH_PARAM.format(param=self.param)
        super().__init__(self.message)


class MissingQueryParamError(PreprocessingError):
    """Exception raised when a required query parameter is missing."""

    def __init__(self, param: str):
        self.param = param
        self.message = ProcessingMessages.Error.MISSING_QUERY_PARAM.format(param=self.param)
        super().__init__(self.message)


class InvalidParameterError(PreprocessingError):
    """Raised when a provided parameter is invalid."""

    def __init__(self, parameter_name):
        super().__init__(ProcessingMessages.Error.INVALID_PARAMETER.format(parameter_name))
        self.parameter_name = parameter_name
