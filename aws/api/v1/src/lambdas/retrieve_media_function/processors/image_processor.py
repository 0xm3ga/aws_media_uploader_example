import logging
from typing import List

from media_processor import MediaProcessor
from shared.constants import error_messages as em
from shared.exceptions import MediaProcessingError
from shared.services.image_processing_service import ImageProcessingInvoker

logger = logging.getLogger(__name__)


class ImageProcessor(MediaProcessor):
    """Processor for image media."""

    def __init__(
        self,
        bucket: str,
        key: str,
        filename: str,
        format: str,
        sizes: List[str],
        username: str,
    ):
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.image_format = format
        self.sizes = sizes
        self.username = username
        self.image_processing_invoker = ImageProcessingInvoker()

    def process(self) -> dict:
        try:
            result = self.image_processing_invoker.invoke_lambda_function(
                self.bucket,
                self.key,
                self.filename,
                self.image_format,
                self.sizes,
            )
            return result
        except Exception as e:
            raise MediaProcessingError(em.ERROR_DURING_PROCESSING_MSG.format(str(e)))
