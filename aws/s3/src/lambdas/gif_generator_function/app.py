import json
import os

import boto3
from botocore.exceptions import NoCredentialsError
from moviepy.editor import VideoFileClip, concatenate_videoclips

from shared.media import Extension

s3_client = boto3.client("s3")
lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    key = event["key"]
    raw_media_bucket = event["bucket"]

    local_file_path = "/tmp/" + key  # Lambda can write to the /tmp directory
    output_path = "/tmp/output.gif"

    # Download the file from S3 to the local filesystem
    s3_client.download_file(raw_media_bucket, key, local_file_path)

    clip = VideoFileClip(local_file_path)
    duration = clip.duration
    frame_times = list(range(0, int(duration), int(duration / 24)))  # 24 frames

    clips = [clip.subclip(t, t + 1) for t in frame_times]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_gif(output_path, fps=24)

    # Upload the processed GIF file to S3
    processed_media_bucket = os.getenv("PROCESSED_MEDIA_BUCKET")
    try:
        s3_client.upload_file(output_path, processed_media_bucket, key)
    except NoCredentialsError:
        return {"Error": "S3 Access Denied"}

    # Trigger the ImageProcessingFunction
    lambda_client.invoke(
        FunctionName="ImageProcessingFunction",
        InvocationType="Event",
        Payload=json.dumps(
            {
                "bucket": processed_media_bucket,
                "format": [Extension.GIF.value],
                "key": key,
            }
        ),
    )
    return {"status": "success"}
