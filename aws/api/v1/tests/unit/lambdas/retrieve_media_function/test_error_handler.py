# from http import HTTPStatus
# from unittest.mock import Mock

# import pytest
# from botocore.exceptions import NoCredentialsError

# from aws.api.v1.src.lambdas.retrieve_media_function import (
#     ObjectNotFoundError,
#     AwsErrorMessages,
#     FileProcessingError,
#     HttpErrorMessages,
#     InvalidTypeError,
#     InvalidValueError,
#     MissingParameterError,
#     PreprocessingError,
#     ProcessingErrorMessages,
#     handle_exception,
#     GeneralErrorMessages,
# )


# @pytest.mark.parametrize(
#     "exception, expected_status, expected_message",
#     [
#         (
#             NoCredentialsError(),
#             HTTPStatus.INTERNAL_SERVER_ERROR,
#             AwsErrorMessages.NO_AWS_CREDENTIALS,
#         ),
#         (
#             PreprocessingError("Test Error"),
#             HTTPStatus.BAD_REQUEST,
#             ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
#         ),
#         (
#             MissingParameterError("Test Param"),
#             HTTPStatus.BAD_REQUEST,
#             ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
#         ),
#         (
#             InvalidTypeError("param", str, int),
#             HTTPStatus.BAD_REQUEST,
#             ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
#         ),
#         (
#             InvalidValueError("param", "not_allowed", ["allowed"]),
#             HTTPStatus.BAD_REQUEST,
#             ProcessingErrorMessages.GENERIC_PROCESSING_ERROR,
#         ),
#         # (
#         #     ObjectNotFoundError(),
#         #     HTTPStatus.NOT_FOUND,
#         #     HttpErrorMessages.OBJECT_NOT_FOUND,
#         # ),
#         (
#             FileProcessingError(),
#             HTTPStatus.INTERNAL_SERVER_ERROR,
#             HttpErrorMessages.INTERNAL_SERVER_ERROR,
#         ),
#         (
#             Exception(
#                 HttpErrorMessages.INTERNAL_SERVER_ERROR,
#             ),
#             HTTPStatus.INTERNAL_SERVER_ERROR,
#             HttpErrorMessages.INTERNAL_SERVER_ERROR,
#         ),
#     ],
# )
# def test_handle_exception(exception, expected_status, expected_message):
#     logger_mock = Mock()
#     status, message = handle_exception(exception, logger_mock)

#     assert status == expected_status
#     assert message == expected_message
#     logger_mock.error.assert_called_once_with(message)


# def test_handle_exception_logging():
#     logger_mock = Mock()
#     exception = Exception(GeneralErrorMessages.UNMAPPED_EXCEPTION)

#     status, message = handle_exception(exception, logger_mock)

#     assert status == HTTPStatus.INTERNAL_SERVER_ERROR
#     assert message == GeneralErrorMessages.UNMAPPED_EXCEPTION
#     logger_mock.error.assert_called_once_with(
#         HttpErrorMessages.INTERNAL_SERVER_ERROR.format(str(GeneralErrorMessages.UNMAPPED_EXCEPTION))
#     )
