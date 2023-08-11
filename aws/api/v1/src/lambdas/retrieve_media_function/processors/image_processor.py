import logging
from typing import List

from shared.constants.error_messages import LambdaErrorMessages
from shared.exceptions import MediaProcessingError
from shared.media.constants import Extension, Size
from shared.services.aws.lambdas.image_processing_service import ImageProcessingInvoker

from .media_processor import MediaProcessor

logger = logging.getLogger(__name__)


class ImageProcessor(MediaProcessor):
    """Processor for image media."""

    def __init__(
        self,
        bucket: str,
        key: str,
        filename: str,
        extension: Extension,
        sizes: List[Size],
        username: str,
    ):
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.extension = extension
        self.sizes = sizes
        self.username = username
        self.image_processing_invoker = ImageProcessingInvoker()

    def process(self) -> dict:
        try:
            result = self.image_processing_invoker.invoke_lambda_function(
                self.bucket,
                self.key,
                self.filename,
                self.extension,
                self.sizes,
            )
            return result
        except Exception as e:
            raise MediaProcessingError(LambdaErrorMessages.ERROR_DURING_PROCESSING.format(str(e)))
