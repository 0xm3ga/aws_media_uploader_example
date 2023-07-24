import json
import os

import boto3


def lambda_handler(event, context):
    # Get bucket name and file key from the S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(bucket)

    # Extract file extension
    _, file_extension = os.path.splitext(key)

    # Depending on the file type, dispatch to the appropriate Lambda function
    if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
        function_name = os.environ.get("IMAGE_PROCESSING_FUNCTION_NAME")
    elif file_extension.lower() in [".mp4", ".avi", ".mov"]:
        function_name = os.environ.get("VIDEO_PROCESSING_FUNCTION_NAME")
    else:
        print(f"Unsupported file type: {file_extension}")
        return

    # Trigger the respective Lambda function
    lambda_client = boto3.client("lambda")
    invoke_response = lambda_client.invoke(
        FunctionName=function_name, InvocationType="Event", Payload=json.dumps(event)
    )
    print(invoke_response)

    return {"statusCode": 200, "body": json.dumps("Processing job started")}
