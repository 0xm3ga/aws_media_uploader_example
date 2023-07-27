import os
import time

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.engine.url import URL

# Define the database connection details
db_url = {
    "drivername": "mysql+pymysql",
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
}

# Create the SQLAlchemy engine
engine = create_engine(URL(**db_url))

# Create a metadata instance
metadata = MetaData()

# Assume your table is named 'media_uploads'
media_uploads = Table("media_uploads", metadata, autoload_with=engine)


def lambda_handler(event, context):
    # Extract bucket name and file key from the event
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_key = event["Records"][0]["s3"]["object"]["key"]

    # Parse username and file type from the file key
    username, file_type, filename = file_key.split("/")

    # Record the upload in RDS
    ins = media_uploads.insert().values(
        username=username,
        filename=filename,
        fileType=file_type,
        timestamp=int(time.time()),  # Unix timestamp
        fileKey=file_key,
        bucket_name=bucket_name,
    )

    with engine.connect() as connection:
        result = connection.execute(ins)
        print(result)
    return {
        "statusCode": 200,
        "body": "Metadata recorded successfully",
    }


lambda_handler({}, {})
