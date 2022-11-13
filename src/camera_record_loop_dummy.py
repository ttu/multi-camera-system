import time
from typing import Callable

from types import VideoCaptureDevice


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id})
    return {"camera_id": camera_id}


def shutdown_camera(dummy_capture: VideoCaptureDevice):
    print("Camera stopping", {"camera_id": dummy_capture["camera_id"]})


def run_camera_loop(
    dummy_capture: VideoCaptureDevice, should_run: Callable[[], bool], should_record: Callable[[], bool]
):
    while should_run():
        if should_record():
            print("Recording", {"camera_id": dummy_capture["camera_id"]})
        time.sleep(1)
