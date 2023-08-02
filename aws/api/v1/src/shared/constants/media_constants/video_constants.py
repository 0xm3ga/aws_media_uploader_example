from enum import Enum


class VideoFormat(Enum):
    MP4 = "mp4"
    MOV = "mov"
    AVI = "avi"
    WMV = "wmv"
    FLV = "flv"

    @property
    def content_type(self):
        return f"video/{self.value}"


class VideoSize(Enum):
    TINY = (120, 120)
    SMALL = (270, 270)
    MEDIUM = (540, 540)
    LARGE = (1080, 1080)
    HUGE = (2160, 2160)


ALLOWED_VIDEO_SIZES = {video_size.name.lower() for video_size in VideoSize}
ALLOWED_VIDEO_FORMATS = {video_format.name.lower() for video_format in VideoFormat}
