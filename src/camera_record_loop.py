from typing import Callable
import cv2

# https://www.geeksforgeeks.org/saving-operated-video-from-a-webcam-using-opencv/


def _create_output():
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
    return out


def _write_to_output(frame, out):
    out.write(frame)


def _release_output(out):
    out.release()


def prepare_camera(camera_id: int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(camera_id)
    return cap


def shutdown_camera(video_capture: cv2.VideoCapture):
    # Release webcam
    video_capture.release()


def run_camera_loop(
    video_capture: cv2.VideoCapture,
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
