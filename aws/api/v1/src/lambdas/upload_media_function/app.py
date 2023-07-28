import json
import os
import uuid

import boto3

s3_client = boto3.client("s3")

# Reference the bucket name from the environment variable
bucket_name = os.environ["RAW_MEDIA_BUCKET"]


def lambda_handler(event, context):
    # Get the user's username from the request context
    username = event["requestContext"]["authorizer"]["claims"]["cognito:username"]

    # Get the file type from the event.
    file_type = event["queryStringParameters"]["type"]

    # Based on the type define the path prefix
    if file_type.startswith("image/"):
        path_prefix = "images/"
    elif file_type.startswith("video/"):
        path_prefix = "videos/"
    else:
        return {"statusCode": 400, "body": "Invalid file type"}

    # Generate a unique filename using UUID
    filename = str(uuid.uuid4())

    if file_type == "image":
        filename = filename + ".jpg"
    elif file_type == "video":
        filename = filename + ".mp4"

    file_key = f"{username}/{path_prefix}{filename}"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": file_key, "ContentType": file_type},
        ExpiresIn=3600,
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"uploadURL": presigned_url, "filename": filename}),
    }
