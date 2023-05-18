import os


SERVER_HOST = os.environ.get("SERVER_HOST", None)
SERVER_PORT = int(os.environ.get("SERVER_PORT", None))
DB_CONNECTION = os.environ.get("DB_CONNECTION", None)
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", None)
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", None)
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", None)
UVICORN_HOST = os.environ.get("UVICORN_HOST", None)
UVICORN_PORT = int(os.environ.get("UVICORN_PORT", None))
UVICORN_BASE_PATH = os.environ.get("UVICORN_BASE_PATH", None)
