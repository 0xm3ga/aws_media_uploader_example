from base_media import BaseMediaFormat, BaseMediaSize, MediaType


class VideoFormat(BaseMediaFormat):
    MP4 = (MediaType.VIDEO.value, "mp4")
    AVI = (MediaType.VIDEO.value, "avi")
    MOV = (MediaType.VIDEO.value, "mov")


class VideoSize(BaseMediaSize):
    TINY = (120, 120)
    SMALL = (270, 270)
    MEDIUM = (540, 540)
    LARGE = (1080, 1080)
    HUGE = (2160, 2160)
