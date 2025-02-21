import os
import time

from typing import Callable

import cv2

import camera_record_loop

from common_types import CameraConfig, CameraStatus, VideoCaptureDevice, VideoFrame, VideoWriter, ViderRecording


VIDEO_1 = f"{camera_record_loop._get_source_path()}{os.sep}sample_videos{os.sep}bike_1_360p.mp4"
VIDEO_2 = f"{camera_record_loop._get_source_path()}{os.sep}sample_videos{os.sep}bike_2_360p.mp4"


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id, "dummy_mode": True})
    video_link = VIDEO_1 if int(camera_id) == 0 else VIDEO_2
    cap = cv2.VideoCapture(video_link)
    cap.set(cv2.CAP_PROP_FPS, 1)
    return VideoCaptureDevice(camera_id, lambda: cap.read(), lambda: cap.release())


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
    video_capture: VideoCaptureDevice, output: VideoWriter, new_frame: Callable[[VideoFrame], None], last_time_ms: float
):
    time_now_ms = time.time() * 1000
    refresh_rate = 1 / 60 * 1000
    elapsed_ms = time_now_ms - last_time_ms
    if elapsed_ms < refresh_rate:
        time.sleep((refresh_rate - elapsed_ms) / 1000)

    _, frame = video_capture.get_frame()
    new_frame(frame)

    return time.time() * 1000


def _recording_state(
    video_capture: VideoCaptureDevice, output: VideoWriter, new_frame: Callable[[VideoFrame], None], last_time_ms: float
):
    time_now_ms = time.time() * 1000
    refresh_rate = 1 / 60 * 1000
    elapsed_ms = time_now_ms - last_time_ms
    if elapsed_ms < refresh_rate:
        time.sleep((refresh_rate - elapsed_ms) / 1000)

    _, frame = video_capture.get_frame()
    new_frame(frame)
    camera_record_loop._write_to_output(frame, output)

    return time.time() * 1000


def run_camera_loop(
    video_capture: VideoCaptureDevice,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
    new_frame: Callable[[VideoFrame], None],
) -> ViderRecording:
    state = CameraStatus.CAMERA_READY
    out = camera_record_loop._create_output(CameraConfig(video_capture.camera_id, (640, 360)))

    last_time = time.time() * 1000
    while True:
        state, state_func = _check_state(state, should_run, should_record, notify_camera_status)
        if not state_func:
            break
        last_time = state_func(video_capture, out, new_frame, last_time)

    camera_record_loop._release_output(out)

    return ViderRecording(out.has_data, out.file_full_name)
