from exceptions import MediaProcessingError, ObjectNotFoundError
from rds import fetch_media_info_from_rds
from utils import construct_raw_media_key, object_exists, process_media
from validation import normalize_extension, validate_extension, validate_size


class MediaRequest:
    def __init__(self, filename: str, size: str, extension: str, raw_media_bucket: str):
        self.filename = filename
        self.size = self._validate_size(size)
        self.extension = self._validate_extension(extension)
        self.raw_media_bucket = raw_media_bucket
        self.username, self.content_type = self._fetch_media_info()

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
            raise ObjectNotFoundError

        # processing
        try:
            key = process_media(
                bucket=self.raw_media_bucket,
                filename=self.filename,
                size=self.size,
                extension=self.extension,
                file_type=self.content_type,
                username=self.username,
            )
        except MediaProcessingError as e:
            raise e

        return key
