import sys
import time
from threading import Thread

from camera_record_listener_db import check_recording_from_db

# from camera_record_loop import prepare_camera, run_camera_loop, shutdown_camera
from camera_record_loop_dummy import prepare_camera, run_camera_loop, shutdown_camera
from camera_send_status_db import update_camera_status
from camera_start_listener_db import check_start_from_db
from camera_types import CameraStatus


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


def _send_status(camera_id: int, status: CameraStatus):
    update_camera_status(camera_id, status)
    print("Sending status:", {camera_id, status.name})


def main_loop(camera_id: int):
    print("Starting:", {camera_id})
    start_thread = Thread(target=_check_camera_on, args=[camera_id])
    start_thread.start()

    _send_status(camera_id, CameraStatus.SYSTEM_STANDBY)

    while True:

        if not _camera_on(camera_id):
            print("idle", {camera_id})
            time.sleep(2)
            continue

        video_capture = prepare_camera(camera_id)
        print("camera ready", {camera_id})
        _send_status(camera_id, CameraStatus.CAMERA_READY)

        RUN_RECORD_CHECK.running = True
        record_thread = Thread(target=_check_recording_on, args=[camera_id])
        record_thread.start()

        run_camera_loop(
            video_capture,
            lambda: _camera_on(camera_id),
            lambda: _recording_on(camera_id),
            lambda status: _send_status(camera_id, status),
        )
        shutdown_camera(video_capture)

        RUN_RECORD_CHECK.running = False
        record_thread.join()

        _send_status(camera_id, CameraStatus.SYSTEM_OFF)


if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else DEFAULT_CAMERA_ID
    main_loop(id)
