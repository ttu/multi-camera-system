from src import file_storage

# Test is for debugging. Requires Minio server with files in bucket


class TestFileStorage:
    def test_get_files(self):
        files = file_storage.get_files()
        assert files is not None
