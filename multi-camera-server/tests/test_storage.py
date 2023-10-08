import pytest

from src import file_storage


@pytest.mark.skip(reason="Test is for debugging. Requires Minio server with files in bucket")
class TestFileStorage:
    def test_get_files(self):
        files = file_storage.get_files()
        assert files is not None

    def test_get_files_prefix(self):
        files = file_storage.get_files("bike_")
        assert len(files) == 2

    def test_get_file_data(self):
        files = file_storage.get_files()
        start = 0
        length = 0
        file = file_storage.get_file_data(files[0], start, length)
        assert file is not None
