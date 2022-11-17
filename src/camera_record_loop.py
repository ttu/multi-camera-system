from typing import Callable

import cv2

from camera_types import CameraStatus, VideoCaptureDevice, VideoWriter

# https://www.geeksforgeeks.org/saving-operated-video-from-a-webcam-using-opencv/


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    print("Camera starting", {"camera_id": camera_id})
    cap = cv2.VideoCapture(camera_id)
    return cap


def shutdown_camera(video_capture: VideoCaptureDevice):
    # Release webcam
    video_capture.release()


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
        if current_state != CameraStatus.RECORDING:
            notify_camera_status(CameraStatus.RECORDING)
        return (CameraStatus.RECORDING, _recording_state)

    if current_state != CameraStatus.READY:
        notify_camera_status(CameraStatus.READY)
    return (CameraStatus.READY, _ready_state)


def _ready_state(video_capture: VideoCaptureDevice, output: VideoWriter):
    # reads frames from a camera
    _, frame = video_capture.read()
    # TODO: Should do something with the frame?
    # Show input frame in the window
    # cv2.imshow("Original", frame)


def _recording_state(video_capture: VideoCaptureDevice, output: VideoWriter):
    _, frame = video_capture.read()
    _write_to_output(frame, output)


def run_camera_loop(
    video_capture: VideoCaptureDevice,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
    notify_camera_status: Callable[[CameraStatus], None],
):
    state = CameraStatus.READY
    out = _create_output()

    while True:
        state, state_func = _check_state(state, should_run, should_record, notify_camera_status)
        if not state_func:
            break
        state_func(video_capture, out)

    _release_output(out)
    # De-allocate any associated memory usage
    # cv2.destroyAllWindows()
