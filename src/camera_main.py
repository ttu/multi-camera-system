import sys
import time
from threading import Thread

from camera_record_listener_db import check_recording_from_db
# from camera_record_loop import prepare_camera, run_camera_loop, shutdown_camera
from camera_record_loop_dummy import prepare_camera, run_camera_loop, shutdown_camera
from camera_start_listener_db import check_start_from_db


class RunFlag:
    running: bool = False


RUN_CAMERA = RunFlag()
RECORD_CAMERA = RunFlag()
RUN_RECORD_CHECK = RunFlag()

# TODO: 2 ids are required. One system wide id and one for device camera id.
DEFAULT_CAMERA_ID = 0


def _camera_on(camera_id: int) -> bool:
    return RUN_CAMERA.running


def _recording_on(camera_id: int) -> bool:
    return RECORD_CAMERA.running


def _check_camera_on(camera_id: int):
    while True:
        should_run = check_start_from_db(camera_id)
        RUN_CAMERA.running = should_run
        time.sleep(2)


def _check_recording_on(camera_id: int):
    while RUN_RECORD_CHECK.running:
        should_record = check_recording_from_db(camera_id)
        RECORD_CAMERA.running = should_record
        time.sleep(1)


def main_loop(camera_id: int):
    start_thread = Thread(target=_check_camera_on, args=[camera_id])
    start_thread.start()

    while True:
        # TODO: Send status "device on"

        if not _camera_on(camera_id):
            print("idle")
            time.sleep(2)
            continue

        video_capture = prepare_camera(camera_id)
        print("camera ready")
        # TODO: Send status "camera ready"

        RUN_RECORD_CHECK.running = True
        record_thread = Thread(target=_check_recording_on, args=[camera_id])
        record_thread.start()

        # TODO: Find a correct place to send status "camera recording"
        run_camera_loop(video_capture, lambda: _camera_on(camera_id), lambda: _recording_on(camera_id))
        shutdown_camera(video_capture)

        RUN_RECORD_CHECK.running = False
        record_thread.join()


if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else DEFAULT_CAMERA_ID
    main_loop(id)
