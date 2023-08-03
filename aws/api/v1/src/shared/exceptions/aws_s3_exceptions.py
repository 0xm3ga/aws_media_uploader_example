from shared.constants.error_messages import S3ErrorMessages


class BaseS3Error(Exception):
    """Base class for exceptions in AWS S3 operations."""

    def __init__(self, message: str):
        super().__init__(message)


class PresignedUrlGenerationError(BaseS3Error):
    """Raised when there is an error generating a presigned URL."""

    def __init__(self, error):
        self.error = error
        message = S3ErrorMessages.FAILED_TO_GENERATE_PRESIGNED_URL.format(error=error)
        super().__init__(message)

    def __str__(self):
        return f"{super().__str__()} - Original error: {self.error}"
