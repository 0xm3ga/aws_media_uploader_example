from shared.media import BaseMedia, BaseMediaFormat, BaseMediaSize, MediaType


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


class VideoMedia(BaseMedia):
    def __init__(self, content_type):
        self.content_type = content_type
        super().__init__(media_type=MediaType.VIDEO)
