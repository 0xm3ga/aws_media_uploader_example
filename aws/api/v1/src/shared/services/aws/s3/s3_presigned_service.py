import logging
import uuid
from typing import Tuple, Union

from shared.constants.error_messages import S3ErrorMessages
from shared.constants.log_messages import S3LogMessages
from shared.constants.media_constants import ImageMedia, VideoMedia
from shared.services.aws.s3.s3_base_service import S3BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class S3PresignService(S3BaseService):
    AWS_OPERATION = "put_object"
    URL_EXPIRATION_SECONDS = 3600

    def generate_presigned_url(
        self,
        media: Union[ImageMedia, VideoMedia],
        username: str,
        raw_bucket_name: str,
    ) -> Tuple[str, str]:
        """Generates a presigned S3 URL for uploading an object."""

        # Generate a unique filename using UUID
        filename = str(uuid.uuid4())

        # Construct the S3 key
        key = self.construct_raw_media_key(
            filename=filename,
            username=username,
            s3_prefix=media.s3_prefix,
        )

        try:
            # Generate a presigned URL for the S3 object
            presigned_url = self.s3_client.generate_presigned_url(
                self.AWS_OPERATION,
                Params={
                    "Bucket": raw_bucket_name,
                    "Key": key,
                    "ContentType": media.content_type,
                },
                ExpiresIn=self.URL_EXPIRATION_SECONDS,
            )
        except Exception as e:
            logger.error(S3ErrorMessages.FAILED_TO_GENERATE_PRESIGNED_URL.format(error=e))
            raise

        logger.info(S3LogMessages.GENERATED_PRESIGNED_URL.format(filename, raw_bucket_name))

        return filename, presigned_url
