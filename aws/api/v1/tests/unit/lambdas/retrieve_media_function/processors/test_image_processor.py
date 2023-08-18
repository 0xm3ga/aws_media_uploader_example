import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.processors.image_processor import (
    Extension,
    ImageProcessor,
    MediaProcessingError,
    Size,
)


@pytest.fixture
def setup_processor(mocker):
    bucket = "test_bucket"
    key = "test_key"
    filename = "test_image.jpg"
    extension = Extension.JPEG
    sizes = [Size.SMALL]
    username = "test_user"

    mock_invoker = mocker.patch(
        "aws.api.v1.src.lambdas.retrieve_media_function.processors.image_processor."
        "ImageProcessingInvoker"
    ).return_value

    return bucket, key, filename, extension, sizes, username, mock_invoker


def test_process_successful_invocation(setup_processor):
    bucket, key, filename, extension, sizes, username, mock_invoker = setup_processor

    mock_result = {"message": "success"}
    mock_invoker.invoke_lambda_function.return_value = mock_result

    processor = ImageProcessor(bucket, key, filename, extension, sizes, username)
    result = processor.process()

    mock_invoker.invoke_lambda_function.assert_called_once_with(
        bucket, key, filename, extension, sizes
    )
    assert result == mock_result


def test_process_with_error(setup_processor):
    bucket, key, filename, extension, sizes, username, mock_invoker = setup_processor

    error_msg = "Lambda invocation error"
    mock_invoker.invoke_lambda_function.side_effect = Exception(error_msg)

    processor = ImageProcessor(bucket, key, filename, extension, sizes, username)

    with pytest.raises(
        MediaProcessingError,
        match=MediaProcessingError().log_message,
    ):
        processor.process()

    mock_invoker.invoke_lambda_function.assert_called_once_with(
        bucket, key, filename, extension, sizes
    )
