from typing import Callable

import cv2

from common_types import CameraStatus, VideoCaptureDevice, VideoFrame, VideoWriter

# https://www.geeksforgeeks.org/saving-operated-video-from-a-webcam-using-opencv/


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id})
    cap = cv2.VideoCapture(camera_id)
    return cap


def shutdown_camera(video_capture: VideoCaptureDevice):
    # Release webcam
    video_capture.release()


def dispaly_show_frame(frame: VideoFrame):
    cv2.imshow("Original", frame)
    cv2.waitKey(1)


def _create_output() -> VideoWriter:
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
    return out


def _write_to_output(frame, out: VideoWriter):
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
    # reads frames from a camera
    _, frame = video_capture.read()
    new_frame(frame)
    # Show input frame in the window
    # cv2.imshow("Original", frame)


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
):
    state = CameraStatus.CAMERA_READY
    out = _create_output()

    while True:
        state, state_func = _check_state(state, should_run, should_record, notify_camera_status)
        if not state_func:
            break
        state_func(video_capture, out, new_frame)

    _release_output(out)
    # De-allocate any associated memory usage
    cv2.destroyAllWindows()
