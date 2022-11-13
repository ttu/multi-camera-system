from typing import Callable
import cv2

from types import VideoCaptureDevice, VideoWriter

# https://www.geeksforgeeks.org/saving-operated-video-from-a-webcam-using-opencv/


def _create_output() -> VideoWriter:
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
    return out


def _write_to_output(frame, out: VideoWriter):
    out.write(frame)


def _release_output(out: VideoWriter):
    out.release()


def prepare_camera(camera_id: int) -> VideoCaptureDevice:
    cap = cv2.VideoCapture(camera_id)
    return cap


def shutdown_camera(video_capture: VideoCaptureDevice):
    # Release webcam
    video_capture.release()


def run_camera_loop(
    video_capture: VideoCaptureDevice,
    should_run: Callable[[], bool],
    should_record: Callable[[], bool],
):
    out = _create_output()

    while should_run():
        # reads frames from a camera
        _, frame = video_capture.read()

        if should_record():
            _write_to_output(frame, out)

        # Show input frame in the window
        # cv2.imshow("Original", frame)

    _release_output(out)
    # De-allocate any associated memory usage
    # cv2.destroyAllWindows()
