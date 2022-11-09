import time
from typing import Any, Callable


def prepare_camera(camera_id: int) -> Any:
    print("Camera starting", {"camera_id": camera_id})
    return {"camera_id": camera_id}


def shutdown_camera(dummy_capture: Any):
    print("Camera stopping", {"camera_id": dummy_capture["camera_id"]})


def run_camera_loop(dummy_capture: Any, should_run: Callable[[], bool], should_record: Callable[[], bool]):
    while should_run():
        if should_record():
            print("Recording", {"camera_id": dummy_capture["camera_id"]})
        time.sleep(1)
