from minio import Minio
from minio.error import S3Error

import common_config
from common_types import FileInfo

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


def get_file_data(file_name: str, offset: int = 0, length: int = 0):
    try:
        video = client.get_object(BUCKET_NAME, file_name, offset=offset, length=length)
        print("File download", {file_name})
        return video
    except S3Error as e:
        print("Error occurred.", e)
        return None


def get_files(prefix: str | None = None) -> list[FileInfo] | None:
    try:
        file_list = client.list_objects(BUCKET_NAME, prefix)
        return [FileInfo(item.object_name, item.size) for item in file_list]
    except S3Error as e:
        print("Error occurred.", e)
        return None
