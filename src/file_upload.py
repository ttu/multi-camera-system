from minio import Minio
from minio.error import S3Error

import common_config

BUCKET_NAME = "camera-system"

# Error: [SSL: WRONG_VERSION_NUMBER] wrong version number
# https://github.com/minio/minio/issues/8161

client = Minio(
    common_config.MINIO_ENDPOINT,
    access_key=common_config.MINIO_ACCESS_KEY,
    secret_key=common_config.MINIO_SECRET_KEY,
    secure=False,
)

if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)


def upload_file(upload_file_name, file_path):
    try:
        client.fput_object(
            BUCKET_NAME,
            upload_file_name,
            file_path,
        )
        print("File uploaded", {upload_file_name, file_path})
    except S3Error as e:
        print("Error occurred.", e)
