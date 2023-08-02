from shared.constants.media_constants.base_media import BaseMediaFormat, BaseMediaSize, MediaType


class ImageFormat(BaseMediaFormat):
    JPEG = (MediaType.IMAGE.value, "jpeg")
    PNG = (MediaType.IMAGE.value, "png")
    GIF = (MediaType.IMAGE.value, "gif")


class ImageSize(BaseMediaSize):
    TINY = (120, 120)
    SMALL = (270, 270)
    MEDIUM = (540, 540)
    LARGE = (1080, 1080)
    HUGE = (2160, 2160)
