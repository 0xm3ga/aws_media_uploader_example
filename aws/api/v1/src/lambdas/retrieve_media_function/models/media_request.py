import logging

import exceptions as ex
from factories.media_processor_factory import MediaProcessorFactory
from services.rds_service import fetch_media_info_from_rds
from utils.aws_s3_utils import construct_raw_media_key, object_exists
from utils.media_processing_utils import convert_content_type_to_file_type
from utils.validation_utils import normalize_extension, validate_extension, validate_size

logger = logging.getLogger(__name__)


class MediaRequest:
    filename: str
    size: str
    extension: str
    raw_media_bucket: str
    username: str
    content_type: str

    def __init__(self, filename: str, size: str, extension: str, raw_media_bucket: str):
        self.filename = filename
        self.size = self._validate_size(size)
        self.extension = self._validate_extension(extension)
        self.raw_media_bucket = raw_media_bucket
        self.username, self.content_type = self._fetch_media_info()
        self.file_type = convert_content_type_to_file_type(self.content_type)

    def _normalize_extension(self, extension: str) -> str:
        return normalize_extension(extension)

    def _validate_size(self, size: str) -> str:
        return validate_size(size)

    def _validate_extension(self, extension: str) -> str:
        normalized_extension = normalize_extension(extension)
        return validate_extension(normalized_extension)

    def _fetch_media_info(self) -> tuple:
        return fetch_media_info_from_rds(self.filename)

    def _constructe_raw_media_key(self) -> str:
        return construct_raw_media_key(self.filename, self.username, self.content_type)

    def process(self) -> str:
        # getting raw media
        key_raw = self._constructe_raw_media_key()
        if not object_exists(self.raw_media_bucket, key_raw):
            raise ex.ObjectNotFoundError

        # processing
        processor = MediaProcessorFactory.create_processor(
            bucket=self.raw_media_bucket,
            key=key_raw,
            filename=self.filename,
            format=self.extension,
            sizes=[self.size],
            username=self.username,
            file_type=self.file_type,
        )
        key = processor.process()

        return str(key)
