import logging
from typing import List

from media_processor import MediaProcessor
from shared.constants.error_messages import LambdaErrorMessages
from shared.constants.media_constants.image import ImageFormat, ImageSize
from shared.exceptions import MediaProcessingError
from shared.services.aws.lambdas.image_processing_service import ImageProcessingInvoker

logger = logging.getLogger(__name__)


class ImageProcessor(MediaProcessor):
    """Processor for image media."""

    def __init__(
        self,
        bucket: str,
        key: str,
        filename: str,
        format: ImageFormat,
        sizes: List[ImageSize],
        username: str,
    ):
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.format = format
        self.sizes = sizes
        self.username = username
        self.image_processing_invoker = ImageProcessingInvoker()

    def process(self) -> dict:
        try:
            result = self.image_processing_invoker.invoke_lambda_function(
                self.bucket,
                self.key,
                self.filename,
                self.format,
                self.sizes,
            )
            return result
        except Exception as e:
            raise MediaProcessingError(LambdaErrorMessages.ERROR_DURING_PROCESSING.format(str(e)))
