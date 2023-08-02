import uuid
from typing import Tuple

import boto3
from shared.constants.media_constants.file_types import FileType
from shared.utils.media_processing_utils import parse_content_type


class S3PresignService:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def generate_presigned_url(
        self, content_type: str, username: str, raw_bucket_name: str
    ) -> Tuple[str, str]:
        primary_type, _ = parse_content_type(content_type)
        # Generate a unique filename using UUID
        filename = str(uuid.uuid4())

        file_type = FileType[primary_type.upper()].value

        key = f"{username}/{file_type}{filename}"

        presigned_url = self.s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": raw_bucket_name,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=3600,
        )

        return filename, presigned_url
