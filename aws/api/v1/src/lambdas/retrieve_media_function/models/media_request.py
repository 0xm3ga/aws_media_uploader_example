import logging

import shared.exceptions as ex
from factories.media_processor_factory import MediaProcessorFactory
from shared.constants.media_constants.media import MediaFormat, MediaSize
from shared.services.aws.rds.rds_service import RdsBaseService
from shared.services.aws.s3.s3_base_service import S3BaseService
from shared.utils.media_factory import MediaFactory

logger = logging.getLogger(__name__)


class MediaRequest:
    filename: str
    size: str
    extension: str
    raw_media_bucket: str

    def __init__(
        self,
        filename: str,
        size: str,
        extension: str,
        raw_media_bucket: str,
    ):
        self.s3_service = S3BaseService()
        self.rds_service = RdsBaseService()
        self.filename = filename
        self.raw_media_bucket = raw_media_bucket

        self.username, self.content_type = self._fetch_media_info()
        self.media = MediaFactory.create_media(self.content_type)

        self.size = MediaSize.validate_size(size)
        self.extension = MediaFormat.validate_extension(extension)

    def _fetch_media_info(self) -> tuple:
        return self.rds_service.fetch_media_info_from_rds(self.filename)

    def process(self) -> str:
        # getting raw media
        key_raw = self.s3_service.construct_raw_media_key(
            filename=self.filename,
            username=self.username,
            s3_prefix=self.media.s3_prefix,
        )
        if not self.s3_service.object_exists(bucket=self.raw_media_bucket, key=key_raw):
            raise ex.ObjectNotFoundError

        # processing
        processor = MediaProcessorFactory.create_processor(
            bucket=self.raw_media_bucket,
            key=key_raw,
            filename=self.filename,
            extension=self.extension,
            sizes=[self.size],
            username=self.username,
            media_type=self.media.media_type,
        )
        processor.process()

        key = self.s3_service.construct_processed_media_key(
            filename=self.filename,
            size=self.size,
            extension=self.extension,
        )

        return key

    def construct_url(self, domain_name: str, key: str):
        return self.s3_service.construct_media_url(domain_name=domain_name, path=key)
