import pytest

from aws.api.v1.src.lambdas.retrieve_media_function.processors.video_processor import (
    Extension,
    FeatureNotImplementedError,
    Size,
    VideoProcessor,
)


def test_video_processor_initialization():
    bucket = "test_bucket"
    key = "test_key"
    filename = "test_video.mp4"
    extension = Extension.MP4
    sizes = [Size.SMALL]
    username = "test_user"

    processor = VideoProcessor(bucket, key, filename, extension, sizes, username)

    assert processor.bucket == bucket
    assert processor.key == key
    assert processor.filename == filename
    assert processor.extension == extension
    assert processor.sizes == sizes
    assert processor.username == username
    assert processor.feature_name == "Video processing"


def test_video_processor_process_raises_not_implemented_error():
    bucket = "test_bucket"
    key = "test_key"
    filename = "test_video.mp4"
    extension = Extension.MP4
    sizes = [Size.SMALL]
    username = "test_user"

    processor = VideoProcessor(bucket, key, filename, extension, sizes, username)

    with pytest.raises(FeatureNotImplementedError, match="Video processing"):
        processor.process()
