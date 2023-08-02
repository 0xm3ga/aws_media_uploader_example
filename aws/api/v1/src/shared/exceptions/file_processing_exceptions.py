from shared.constants.error_messages import (
    ERROR_DURING_PROCESSING_MSG,
    ERROR_INVOKING_LAMBDA_MSG,
    ERROR_PROCESSING_RESPONSE_MSG,
    ERROR_UNSUPPORTED_FILE_TYPE_MSG,
    FEATURE_NOT_IMPLEMENTED_ERROR_MSG,
    FILE_PROCESSING_ERROR_MSG,
)

from .base_exceptions import CustomException


class MediaProcessingError(CustomException):
    """Base class for exceptions related to media processing."""

    pass


class FileProcessingError(CustomException):
    """Exception raised during file processing."""

    def __init__(self, message=FILE_PROCESSING_ERROR_MSG):
        self.message = message
        super().__init__(message)


class LambdaInvocationError(MediaProcessingError):
    """Raised when there is an error invoking the Lambda function."""

    def __init__(self, details=""):
        super().__init__(ERROR_INVOKING_LAMBDA_MSG.format(details))


class LambdaResponseProcessingError(MediaProcessingError):
    """Raised when there is an error processing the Lambda function response."""

    def __init__(self, details=""):
        super().__init__(ERROR_PROCESSING_RESPONSE_MSG.format(details))


class ProcessingError(MediaProcessingError):
    """Raised when there is an error during processing."""

    def __init__(self, details=""):
        super().__init__(ERROR_DURING_PROCESSING_MSG.format(details))


class UnsupportedFileTypeError(MediaProcessingError):
    """Raised when the file type is not supported."""

    def __init__(self, details=""):
        super().__init__(ERROR_UNSUPPORTED_FILE_TYPE_MSG.format(details))


class FeatureNotImplementedError(CustomException):
    """Raised when a feature is not yet implemented."""

    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        self.message = FEATURE_NOT_IMPLEMENTED_ERROR_MSG.format(feature_name=feature_name)
        super().__init__(self.message)
