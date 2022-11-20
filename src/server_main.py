import time
from dataclasses import dataclass
from threading import Thread

import cv2

from server_check_status_db import check_status_from_db
from server_toggle_start import set_camera_running
from video_stream_consumer import receive_stream


@dataclass
class CameraConfig:
    route_id: int
    cameras: list[int]


c = CameraConfig(1, [0, 1])


def _check_status(camera_config: CameraConfig):
    while True:
        for camera_id in camera_config.cameras:
            status = check_status_from_db(camera_id)
            print("Camera status", {"camera_id": camera_id, "status": status})
            time.sleep(2.1)


def _handle_video_stream():
    for frame in receive_stream():
        cv2.imshow("server", frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


def main_loop():
    print("Server starting")
    check_thread = Thread(target=_check_status, args=[c], daemon=True)
    check_thread.start()
    stream_thread = Thread(target=_handle_video_stream, daemon=True)
    stream_thread.start()

    # TODO: Receive start signal from API
    set_camera_running(0, True)

    while True:
        print("Server waiting")

        time.sleep(2)


if __name__ == "__main__":
    main_loop()
