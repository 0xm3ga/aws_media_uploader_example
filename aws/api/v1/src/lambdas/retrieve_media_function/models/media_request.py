import logging
from typing import Tuple, Union

import shared.exceptions as ex
from factories.media_processor_factory import MediaProcessorFactory
from shared.constants.media_constants import ImageMedia, MediaFormat, MediaSize, VideoMedia
from shared.services.aws.rds.rds_service import RdsBaseService
from shared.services.aws.s3.s3_base_service import S3BaseService
from shared.utils.media_factory import MediaFactory

logger = logging.getLogger(__name__)


class MediaRequest:
    def __init__(self, processed_media_bucket: str, raw_media_bucket: str, domain_name: str):
        self.s3_service = S3BaseService()
        self.rds_service = RdsBaseService()
        self.processed_media_bucket = processed_media_bucket
        self.raw_media_bucket = raw_media_bucket
        self.domain_name = domain_name

    def process(self, filename: str, size: str, extension: str) -> str:
        # validate inputs
        size = MediaSize.validate_size(size)
        extension = MediaFormat.validate_extension(extension)

        # construct processed key
        processed_key = self._construct_processed_key(filename, size, extension)

        # checking if already processed
        if self._check_object_exists(self.processed_media_bucket, processed_key):
            # get info to construct raw key
            username, content_type = self._fetch_media_info(filename)
            media = MediaFactory.create_media(content_type)  # TODO: refactor

            # check if exists in raw bucket
            raw_key = self._construct_raw_key(filename, username, media.s3_prefix)
            self._check_object_exists(bucket=self.raw_media_bucket, key=raw_key, required=True)

            # process
            processor = self._create_processor(filename, extension, username, media, raw_key, size)
            processor.process()

        # return url
        return self._construct_url(processed_key)

    def _fetch_media_info(self, filename: str) -> Tuple[str, str]:
        try:
            return self.rds_service.fetch_media_info_from_rds(filename)
        except Exception as e:
            logger.error(f"Error fetching media info: {str(e)}")
            raise

    def _construct_raw_key(self, filename: str, username: str, s3_prefix: str) -> str:
        return self.s3_service.construct_raw_media_key(
            filename=filename,
            username=username,
            s3_prefix=s3_prefix,
        )

    def _construct_processed_key(self, filename: str, size: str, extension: str) -> str:
        return self.s3_service.construct_processed_media_key(
            filename=filename,
            size=size,
            extension=extension,
        )

    def _check_object_exists(self, bucket: str, key: str, required: bool = False) -> bool:
        if not self.s3_service.object_exists(bucket=bucket, key=key):
            if required:
                raise ex.ObjectNotFoundError
            return False
        return True

    def _create_processor(
        self,
        filename: str,
        extension: str,
        username: str,
        media: Union[ImageMedia, VideoMedia],
        raw_key: str,
        size: str,
    ):
        return MediaProcessorFactory.create_processor(
            bucket=self.raw_media_bucket,
            key=raw_key,
            filename=filename,
            extension=extension,
            sizes=[size],
            username=username,
            media_type=media.media_type,
        )

    def _construct_url(self, key: str) -> str:
        return self.s3_service.construct_media_url(domain_name=self.domain_name, path=key)
