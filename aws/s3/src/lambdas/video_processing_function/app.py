import os
import uuid

import boto3
from moviepy.editor import VideoFileClip

s3 = boto3.client("s3")


# For more complex video processing tasks, you might want to consider using other AWS services


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        download_path = "/tmp/{}{}".format(uuid.uuid4(), key)
        upload_path = "/tmp/processed-{}".format(key)

        s3.download_file(bucket, key, download_path)
        process_video(download_path, upload_path)
        s3.upload_file(upload_path, os.getenv("PROCESSED_MEDIA_BUCKET"), key)


def process_video(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec="libx264")
