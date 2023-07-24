import os
import uuid

import boto3
from PIL import Image

# import io

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        download_path = "/tmp/{}{}".format(uuid.uuid4(), key)
        upload_path = "/tmp/resized-{}".format(key)

        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, os.getenv("PROCESSED_MEDIA_BUCKET"), key)


def resize_image(download_path, upload_path, size=(1280, 720)):
    with Image.open(download_path) as img:
        img.thumbnail(size)
        img.save(upload_path)
