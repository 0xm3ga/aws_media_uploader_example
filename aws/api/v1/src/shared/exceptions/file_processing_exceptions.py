from http import HTTPStatus

from shared.constants.logging_messages import GeneralMessages, LambdaMessages, ProcessingMessages

from .exceptions import AppError


class MediaProcessingError(AppError):
    """Base class for exceptions related to media processing."""

    def __init__(self, user_message, log_message, http_status, **log_args):
        super().__init__(user_message, log_message, http_status, log_args)


class FileProcessingError(MediaProcessingError):
    """Exception raised during file processing."""

    def __init__(self, message=ProcessingMessages.Error.GENERIC_PROCESSING_ERROR):
        super().__init__(
            user_message=message,
            log_message=message,
            http_status=HTTPStatus.BAD_REQUEST,
        )


class LambdaInvocationError(MediaProcessingError):
    """Raised when there is an error invoking the Lambda function."""

    def __init__(self, details=""):
        log_args = {"details": details}
        super().__init__(
            user_message="Error invoking Lambda function.",
            log_message=LambdaMessages.Error.ERROR_INVOKING_LAMBDA.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )


class LambdaResponseProcessingError(MediaProcessingError):
    """Raised when there is an error processing the Lambda function response."""

    def __init__(self, details=""):
        log_args = {"details": details}
        super().__init__(
            user_message="Error processing Lambda function response.",
            log_message=LambdaMessages.Error.ERROR_PROCESSING_RESPONSE.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )


class ProcessingError(MediaProcessingError):
    """Raised when there is an error during processing."""

    def __init__(self, details=""):
        log_args = {"details": details}
        super().__init__(
            user_message="Error during processing.",
            log_message=LambdaMessages.Error.ERROR_DURING_PROCESSING.format(**log_args),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            log_args=log_args,
        )


class UnsupportedFileTypeError(MediaProcessingError):
    """Raised when the file type is not supported."""

    def __init__(self, details=""):
        log_args = {"details": details}
        super().__init__(
            user_message="Unsupported file type.",
            log_message=LambdaMessages.Error.ERROR_UNSUPPORTED_FILE_TYPE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class FeatureNotImplementedError(AppError):
    """Raised when a feature is not yet implemented."""

    def __init__(self, feature_name: str):
        log_args = {"feature_name": feature_name}
        super().__init__(
            user_message=f"Feature '{feature_name}' not implemented.",
            log_message=GeneralMessages.Error.FEATURE_NOT_IMPLEMENTED.format(**log_args),
            http_status=HTTPStatus.NOT_IMPLEMENTED,
            log_args=log_args,
        )
