import os
import pathlib
import time
from typing import Callable

import cv2

from common_types import CameraStatus, VideoCaptureDevice, VideoFrame

current_path = str(pathlib.Path().resolve())
PATH = current_path if current_path.endswith("src") else f"{current_path}{os.sep}src"


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id})
    return {"camera_id": camera_id}


def shutdown_camera(dummy_capture: VideoCaptureDevice):
    print("Camera stopping", {"camera_id": dummy_capture["camera_id"]})


# pylint: disable-next=unused-argument
def dispaly_show_frame(frame: VideoFrame):
    print("Showing new frame")


def _check_state(
    current_state: CameraStatus,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
):
    if not should_run():
        return (None, None)

    if should_record():
        if current_state != CameraStatus.CAMERA_RECORDING:
            notify_camera_status(CameraStatus.CAMERA_RECORDING)
        return (CameraStatus.CAMERA_RECORDING, _recording_state)

    if current_state != CameraStatus.CAMERA_READY:
        notify_camera_status(CameraStatus.CAMERA_READY)
    return (CameraStatus.CAMERA_READY, _ready_state)


def _get_frame():
    image = cv2.imread(f"{PATH}/images/cat.jpg")
    return image


def _ready_state(dummy_capture: VideoCaptureDevice, new_frame: Callable[[VideoFrame], None]):
    print("Waiting for signal", {"camera_id": dummy_capture["camera_id"]})
    frame = _get_frame()
    new_frame(frame)


def _recording_state(dummy_capture: VideoCaptureDevice, new_frame: Callable[[VideoFrame], None]):
    print("Recording", {"camera_id": dummy_capture["camera_id"]})
    frame = _get_frame()
    new_frame(frame)


def run_camera_loop(
    dummy_capture: VideoCaptureDevice,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
    new_frame: Callable[[VideoFrame], None],
):
    state = CameraStatus.CAMERA_READY
    while True:
        state, state_func = _check_state(state, should_run, should_record, notify_camera_status)
        if not state_func:
            break
        state_func(dummy_capture, new_frame)
        time.sleep(1)
