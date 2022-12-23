import os
import pathlib
import time
from typing import Callable

import cv2

from common_types import CameraStatus, VideoCaptureDevice, VideoFrame, VideoWriter, ViderRecording

# https://www.geeksforgeeks.org/saving-operated-video-from-a-webcam-using-opencv/

# pylint: disable=duplicate-code, unused-argument

current_path = str(pathlib.Path().resolve())
source_path = current_path if current_path.endswith("src") else f"{current_path}{os.sep}src"
video_record_path = f"{source_path}{os.sep}temp_video{os.sep}"
video_record_file_name = "output.avi"


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id})
    cap = cv2.VideoCapture(camera_id)
    return cap


def shutdown_camera(video_capture: VideoCaptureDevice):
    video_capture.release()


def _create_output() -> VideoWriter:
    file_name = f"record_{round(time.time())}.avi"
    file_full_path = f"{video_record_path}{file_name}"

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(file_full_path, fourcc, 20.0, (640, 480))
    return VideoWriter(out, file_full_path)


def _write_to_output(frame: VideoFrame, out: VideoWriter):
    out.write(frame)


def _release_output(out: VideoWriter):
    out.release()


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


def _ready_state(
    video_capture: VideoCaptureDevice,
    output: VideoWriter,
    new_frame: Callable[[VideoFrame], None],
):
    _, frame = video_capture.read()
    new_frame(frame)


def _recording_state(
    video_capture: VideoCaptureDevice,
    output: VideoWriter,
    new_frame: Callable[[VideoFrame], None],
):
    _, frame = video_capture.read()
    new_frame(frame)
    _write_to_output(frame, output)


def run_camera_loop(
    video_capture: VideoCaptureDevice,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
    new_frame: Callable[[VideoFrame], None],
) -> ViderRecording:
    state = CameraStatus.CAMERA_READY
    out = _create_output()

    while True:
        state, state_func = _check_state(state, should_run, should_record, notify_camera_status)
        if not state_func:
            break
        state_func(video_capture, out, new_frame)

    _release_output(out)

    return ViderRecording(out.has_data, out.file_full_name)
