from image import ImageFormat, ImageSize
from video import VideoFormat, VideoSize


class MediaFormat:
    @staticmethod
    def allowed_content_types():
        return set(ImageFormat.allowed_content_types()).union(VideoFormat.allowed_content_types())

    @staticmethod
    def allowed_extensions():
        return set(ImageFormat.allowed_extensions()).union(VideoFormat.allowed_extensions())


class MediaSize:
    @staticmethod
    def allowed_sizes():
        return set(ImageSize.allowed_sizes()).union(VideoSize.allowed_sizes())

    @staticmethod
    def allowed_dimensions():
        return set(ImageSize.allowed_dimensions()).union(VideoSize.allowed_dimensions())
