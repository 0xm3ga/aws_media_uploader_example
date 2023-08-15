from http import HTTPStatus

from shared.constants.logging_messages import ProcessingMessages, RdsMessages

from .exceptions import AppError


class PreprocessingError(AppError):
    """Exception raised for preprocessing errors."""

    def __init__(self, user_message, log_message, http_status, **log_args):
        super().__init__(user_message, log_message, http_status, **log_args)


class UnsupportedExtensionError(PreprocessingError):
    """Exception raised when an unsupported file extension is encountered."""

    def __init__(self, extension: str):
        log_args = {"extension": extension}
        super().__init__(
            user_message=f"Unsupported file extension: {extension}",
            log_message=ProcessingMessages.Error.UNSUPPORTED_EXTENSION.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class UnsupportedSizeError(PreprocessingError):
    """Exception raised when an unsupported size is encountered."""

    def __init__(self, size: str):
        log_args = {"size": size}
        super().__init__(
            user_message=f"Unsupported size: {size}",
            log_message=ProcessingMessages.Error.UNSUPPORTED_SIZE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class MissingRequiredRDSVariablesError(PreprocessingError):
    """Exception raised when required variables are missing in the response from RDS."""

    def __init__(self, missing_data: str):
        log_args = {"missing_data": missing_data}
        super().__init__(
            user_message=f"Missing required RDS variables: {missing_data}",
            log_message=RdsMessages.Error.INVALID_RDS_RESPONSE.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class MissingPathParamError(PreprocessingError):
    """Exception raised when a required path parameter is missing."""

    def __init__(self, param: str):
        log_args = {"param": param}
        super().__init__(
            user_message=f"Missing path parameter: {param}",
            log_message=ProcessingMessages.Error.MISSING_PATH_PARAM.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class MissingQueryParamError(PreprocessingError):
    """Exception raised when a required query parameter is missing."""

    def __init__(self, param: str):
        log_args = {"param": param}
        super().__init__(
            user_message=f"Missing query parameter: {param}",
            log_message=ProcessingMessages.Error.MISSING_QUERY_PARAM.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )


class InvalidParameterError(PreprocessingError):
    """Raised when a provided parameter is invalid."""

    def __init__(self, parameter_name):
        log_args = {"parameter_name": parameter_name}
        super().__init__(
            user_message=f"Invalid parameter: {parameter_name}",
            log_message=ProcessingMessages.Error.INVALID_PARAMETER.format(**log_args),
            http_status=HTTPStatus.BAD_REQUEST,
            log_args=log_args,
        )
