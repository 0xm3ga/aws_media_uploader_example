from utils import get_content_type, get_extension_from_content_type


class ImageMedia:
    def __init__(self, s3_client, bucket, key, filename):
        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        self.filename = filename
        self.content_type = get_content_type(self.s3_client, self.bucket, self.key)
        self.extension = get_extension_from_content_type(self.content_type)
