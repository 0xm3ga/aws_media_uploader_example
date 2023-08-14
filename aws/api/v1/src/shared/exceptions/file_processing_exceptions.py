from shared.constants.logging_messages import GeneralMessages, LambdaMessages, ProcessingMessages

from .base_exceptions import CustomException


class MediaProcessingError(CustomException):
    """Base class for exceptions related to media processing."""

    pass


class FileProcessingError(CustomException):
    """Exception raised during file processing."""

    def __init__(self, message=ProcessingMessages.Error.GENERIC_PROCESSING_ERROR):
        self.message = message
        super().__init__(message)


class LambdaInvocationError(MediaProcessingError):
    """Raised when there is an error invoking the Lambda function."""

    def __init__(self, details=""):
        super().__init__(LambdaMessages.Error.ERROR_INVOKING_LAMBDA.format(details))


class LambdaResponseProcessingError(MediaProcessingError):
    """Raised when there is an error processing the Lambda function response."""

    def __init__(self, details=""):
        super().__init__(LambdaMessages.Error.ERROR_PROCESSING_RESPONSE.format(details))


class ProcessingError(MediaProcessingError):
    """Raised when there is an error during processing."""

    def __init__(self, details=""):
        super().__init__(LambdaMessages.Error.ERROR_DURING_PROCESSING.format(details))


class UnsupportedFileTypeError(MediaProcessingError):
    """Raised when the file type is not supported."""

    def __init__(self, details=""):
        super().__init__(LambdaMessages.Error.ERROR_UNSUPPORTED_FILE_TYPE.format(details))


class FeatureNotImplementedError(CustomException):
    """Raised when a feature is not yet implemented."""

    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        self.message = GeneralMessages.Error.FEATURE_NOT_IMPLEMENTED.format(
            feature_name=feature_name
        )
        super().__init__(self.message)
