from base_exceptions import CustomException


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
