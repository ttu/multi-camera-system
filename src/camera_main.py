import argparse
import socket
import time
from threading import Thread

import data_store
import event_handler
import file_upload
import video_stream_producer
from common_types import CameraStatus, EventType, VideoFrame

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--camera-id", dest="camera_id", default=0)
arg_parser.add_argument("--dummy-mode", dest="use_dummy_mode", default=False)

# pylint: disable=import-outside-toplevel, no-else-return


class RunFlag:
    running: bool = False


RUN_CAMERA = RunFlag()
STREAM_CAMERA = RunFlag()
STREAM_CAMERA.running = True
RECORD_CAMERA = RunFlag()


# TODO: 2 ids are required. One system wide id and one for device camera id.
DEFAULT_CAMERA_ID = 0


# pylint: disable-next=unused-argument
def _camera_on(camera_id: int) -> bool:
    return RUN_CAMERA.running


# pylint: disable-next=unused-argument
def _recording_on(camera_id: int) -> bool:
    return RECORD_CAMERA.running


def _listen_camera_events(camera_id: int):
    while True:
        for event, _ in event_handler.wait_for_events(
            [EventType.CAMERA_PREPARE, EventType.CAMERA_TURNOFF, EventType.CAMERA_RECORD, EventType.CAMERA_STOP_RECORD],
            camera_id,
        ):
            # should_run = get_camera_running(camera_id)
            if event in [EventType.CAMERA_PREPARE.value, EventType.CAMERA_TURNOFF.value]:
                RUN_CAMERA.running = event == EventType.CAMERA_PREPARE.value
                data_store.update_camera_running(camera_id, RUN_CAMERA.running)
            elif event in [EventType.CAMERA_RECORD.value, EventType.CAMERA_STOP_RECORD.value]:
                RECORD_CAMERA.running = event == EventType.CAMERA_RECORD.value
                data_store.update_camera_recording(camera_id, RECORD_CAMERA.running)


def _send_status(camera_id: int, status: CameraStatus):
    data_store.update_camera_status(camera_id, status)
    print("Sending status:", {camera_id, status.name})


def _update_address_info(camera_id: int, socket: socket.socket | None):
    local_address = socket.getsockname() if socket else None
    address = f"{local_address[0]}:{local_address[1]}" if local_address else None
    data_store.update_camera_address(camera_id, address)
    event_handler.send_event(EventType.CAMERA_ADDRESS_UPDATE, camera_id, address)
    print("Update address", {"camera_id": camera_id, "address": address})


def _new_frame_received(socket: socket.socket | None, frame: VideoFrame):
    if STREAM_CAMERA.running and socket:
        video_stream_producer.send_frame(socket, frame)
        # dispaly_show_frame(frame)


def _send_video_to_storage(file_path: str):
    save_as_file_name = f"video_{round(time.time())}.avi"
    file_upload.upload_file(save_as_file_name, file_path)


def _get_camera_functions(use_dummy_mode: bool):
    if use_dummy_mode:
        from camera_record_loop_dummy import prepare_camera, run_camera_loop, shutdown_camera

        return prepare_camera, run_camera_loop, shutdown_camera
    else:
        from camera_record_loop import prepare_camera, run_camera_loop, shutdown_camera  # type: ignore

        return prepare_camera, run_camera_loop, shutdown_camera


def main_loop(camera_id: int, use_dummy_mode: bool):
    print("Starting:", {"camera_id": camera_id, "use_dummy_mode": use_dummy_mode})
    prepare_camera, run_camera_loop, shutdown_camera = _get_camera_functions(use_dummy_mode)

    event_thread = Thread(target=_listen_camera_events, args=[camera_id], daemon=True)
    event_thread.start()

    socket = None

    _send_status(camera_id, CameraStatus.SYSTEM_STANDBY)
    _update_address_info(camera_id, socket)

    while True:

        if not _camera_on(camera_id):
            print("idle", {"camera_id": camera_id})
            time.sleep(2)
            continue

        _send_status(camera_id, CameraStatus.CAMERA_PREPARE)

        if not socket:
            socket = video_stream_producer.try_init_socket()
            _update_address_info(camera_id, socket)

        video_capture = prepare_camera(camera_id)
        print("camera ready", {"camera_id": camera_id})
        _send_status(camera_id, CameraStatus.CAMERA_READY)

        record_info = run_camera_loop(
            video_capture,
            lambda: _camera_on(camera_id),
            lambda: _recording_on(camera_id),
            lambda status: _send_status(camera_id, status),
            lambda frame: _new_frame_received(socket, frame),
        )
        shutdown_camera(video_capture)

        _send_status(camera_id, CameraStatus.SYSTEM_STANDBY)
        _send_video_to_storage(record_info)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main_loop(args.camera_id, args.use_dummy_mode)
