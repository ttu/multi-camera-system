from unittest.mock import patch

from fastapi.testclient import TestClient

from common_types import FileInfo
from src.server_main import app


client = TestClient(app)


class TestServer:
    def test_get_route_info(self):
        response = client.get("/route-info/")
        assert response.status_code == 200

        content = response.json()
        assert content == []

    @patch("file_storage.get_files", return_value=[FileInfo("bike_1.mp4", 1000)])
    def test_get_video_files(self, _):
        response = client.get("/video-files/")
        assert response.status_code == 200

        content = response.json()
        assert len(content["files"]) == 1
