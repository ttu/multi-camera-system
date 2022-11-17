import time
from typing import Callable

from camera_types import CameraStatus, VideoCaptureDevice


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id})
    return {"camera_id": camera_id}


def shutdown_camera(dummy_capture: VideoCaptureDevice):
    print("Camera stopping", {"camera_id": dummy_capture["camera_id"]})


def _check_state(
    current_state: CameraStatus,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
):
    if not should_run():
        return (None, None)

    if should_record():
        if current_state != CameraStatus.RECORDING:
            notify_camera_status(CameraStatus.RECORDING)
        return (CameraStatus.RECORDING, _recording_state)

    if current_state != CameraStatus.READY:
        notify_camera_status(CameraStatus.READY)
    return (CameraStatus.READY, _ready_state)


def _ready_state(dummy_capture: VideoCaptureDevice):
    print("Waiting for signal", {"camera_id": dummy_capture["camera_id"]})


def _recording_state(dummy_capture: VideoCaptureDevice):
    print("Recording", {"camera_id": dummy_capture["camera_id"]})


def run_camera_loop(
    dummy_capture: VideoCaptureDevice,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
):
    state = CameraStatus.READY
    while True:
        state, state_func = _check_state(state, should_run, should_record, notify_camera_status)
        if not state_func:
            break
        state_func(dummy_capture)
        time.sleep(1)
