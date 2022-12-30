from src import file_storage

# Test is for debugging. Requires Minio server with files in bucket


class TestFileStorage:
    def test_get_files(self):
        files = file_storage.get_file_names()
        assert files is not None

    def test_download_file(self):
        files = file_storage.get_file_names()
        file = file_storage.get_file_data(files[0])
        assert file is not None
