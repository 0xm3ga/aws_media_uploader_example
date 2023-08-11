from unittest.mock import Mock, patch

import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.factories.media_processor_factory import (
    Extension,
    ImageProcessor,
    MediaProcessorFactory,
    Size,
    UnsupportedFileTypeError,
    VideoProcessor,
)

MEDIA_TYPE_PATH = (
    "aws.api.v1.src.lambdas.retrieve_media_function.factories.media_processor_factory.MediaType"
)


def test_create_image_processor():
    bucket, key, filename, extension, sizes, username = (
        "test_bucket",
        "test_key",
        "test_file.jpg",
        Extension.JPEG,
        [Size.SMALL],
        "test_user",
    )

    processor = MediaProcessorFactory.create_processor(
        bucket, key, filename, extension, sizes, username
    )

    assert isinstance(processor, ImageProcessor)
    assert processor.bucket == bucket
    assert processor.key == key


def test_create_video_processor():
    bucket, key, filename, extension, sizes, username = (
        "test_bucket",
        "test_key",
        "test_file.mp4",
        Extension.MP4,
        [Size.SMALL],
        "test_user",
    )

    processor = MediaProcessorFactory.create_processor(
        bucket, key, filename, extension, sizes, username
    )

    assert isinstance(processor, VideoProcessor)
    assert processor.bucket == bucket
    assert processor.key == key


def test_create_unsupported_processor():
    bucket, key, filename, extension, sizes, username = (
        "test_bucket",
        "test_key",
        "test_file.txt",
        Extension.JPEG,
        [Size.SMALL],
        "test_user",
    )

    class MockMediaTypeEnum:
        UNKNOWN = Mock(value="UNKNOWN")
        IMAGE = Mock(value="IMAGE")
        VIDEO = Mock(value="VIDEO")

    with patch(
        MEDIA_TYPE_PATH,
        new=MockMediaTypeEnum,
    ):
        with pytest.raises(UnsupportedFileTypeError):
            MediaProcessorFactory.create_processor(
                bucket, key, filename, extension, sizes, username
            )
