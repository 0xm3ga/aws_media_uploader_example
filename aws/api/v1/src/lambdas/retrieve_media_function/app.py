# import os
import base64

import boto3
from botocore.exceptions import NoCredentialsError


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    try:
        bucket_name = "media.bluecollarverse.com-processed"  # os.environ["PROCESSED_MEDIA_BUCKET"]
        filename = event["pathParameters"]["filename"]  # fetch filename from the url path parameter

        queryStringParameters = event.get("queryStringParameters") or {}
        size = queryStringParameters.get("size", "medium")
        extension = queryStringParameters.get("extension", "jpg")

        # List of accepted sizes
        accepted_sizes = ["small", "medium", "large"]

        # List of accepted formats
        accepted_formats = ["jpg", "jpeg", "png", "gif"]

        if size not in accepted_sizes:
            size = "medium"

        # Check if the provided format is in the list of accepted formats. If not, default to 'jpg'.
        if extension not in accepted_formats:
            extension = "jpg"
    except Exception as e:
        return {"statusCode": 500, "body": f"Preprocessing error: {str(e)}"}

    try:
        # Construct the key
        key = f"{filename}/{size}.{extension}"

        # OPTION 1
        # # Generate signed URL
        # url = f"https://{bucket_name}.s3.amazonaws.com/{key}"

        # # Return a 302 redirect to the signed URL
        # return {
        #     "statusCode": 302,
        #     "headers": {
        #         "Location": url,
        #     },
        # }

        # OPTION 2:
        # Download the image from S3
        file_object = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = file_object["Body"].read()

        # Convert the image to base64
        base64_image = base64.b64encode(file_content).decode("utf-8")

        # Determine the content type for the response
        if extension == "jpg" or extension == "jpeg":
            content_type = "image/jpeg"
        elif extension == "png":
            content_type = "image/png"
        elif extension == "gif":
            content_type = "image/gif"
        else:
            content_type = "image/jpeg"

        # Return the image as the response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": content_type,
            },
            "body": base64_image,
            "isBase64Encoded": True,
        }

    except NoCredentialsError:
        return {"statusCode": 403, "body": "No AWS credentials found"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
