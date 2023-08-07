from shared.constants.error_messages import ProcessingErrorMessages

from .base_exceptions import CustomException


class InvalidImageFormatError(CustomException):
    """Exception raised when an unsupported image format is encountered."""

    def __init__(self, extension: str):
        super().__init__(ProcessingErrorMessages.UNSUPPORTED_EXTENSION.format(extension))


class InvalidImageSizeError(CustomException):
    """Exception raised when an unsupported image size is encountered."""

    def __init__(self, size: str):
        super().__init__(ProcessingErrorMessages.UNSUPPORTED_SIZE.format(size))


class InvalidMediaTypeError(ValueError):
    pass


class InvalidExtensionError(ValueError):
    pass


class InvalidContentTypeError(ValueError):
    pass
