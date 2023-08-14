import logging
import uuid
from typing import Tuple, Union

from shared.constants.logging_messages import S3Messages
from shared.media.base import ImageMedia, VideoMedia
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
            logger.error(S3Messages.Error.FAILED_TO_GENERATE_PRESIGNED_URL.format(error=str(e)))
            raise

        logger.info(S3Messages.Info.GENERATED_PRESIGNED_URL.format(filename=filename))

        return filename, presigned_url
