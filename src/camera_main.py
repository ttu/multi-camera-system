import argparse
import socket
import time
from threading import Thread
from typing import Callable

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


class SocketWrapper:
    socket_object: socket.socket | None = None


RUN_CAMERA = RunFlag()
STREAM_CAMERA = RunFlag()
STREAM_CAMERA.running = True
RECORD_CAMERA = RunFlag()

SOCKET = SocketWrapper()

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
            [
                EventType.CAMERA_COMMAND_PREPARE,
                EventType.CAMERA_COMMAND_TURNOFF,
                EventType.CAMERA_COMMAND_RECORD,
                EventType.CAMERA_COMMAND_STOP_RECORD,
            ],
            camera_id,
        ):
            # should_run = get_camera_running(camera_id)
            if event in [EventType.CAMERA_COMMAND_PREPARE.value, EventType.CAMERA_COMMAND_TURNOFF.value]:
                RUN_CAMERA.running = event == EventType.CAMERA_COMMAND_PREPARE.value
                data_store.update_camera_running(camera_id, RUN_CAMERA.running)
            elif event in [EventType.CAMERA_COMMAND_RECORD.value, EventType.CAMERA_COMMAND_STOP_RECORD.value]:
                RECORD_CAMERA.running = event == EventType.CAMERA_COMMAND_RECORD.value
                data_store.update_camera_recording(camera_id, RECORD_CAMERA.running)


def _send_status(camera_id: int, status: CameraStatus):
    data_store.update_camera_status(camera_id, status)
    event_handler.send_event(EventType.CAMERA_UPDATE_STATUS, camera_id, status.name)
    print("Update status", {"camera_id": camera_id, "status": status.name})


def _update_address_info(camera_id: int, s: socket.socket | None):
    local_address = s.getsockname() if s else None
    address = f"{local_address[0]}:{local_address[1]}" if local_address else None
    data_store.update_camera_address(camera_id, address)
    event_handler.send_event(EventType.CAMERA_UPDATE_ADDRESS, camera_id, address or "")
    print("Update address", {"camera_id": camera_id, "address": address})


def _new_frame_received(s: socket.socket | None, frame: VideoFrame, request_socket_update: Callable[[], None]):
    s = s if s else request_socket_update()
    if STREAM_CAMERA.running and s:
        success = video_stream_producer.send_frame(s, frame)
        if not success:
            request_socket_update()


def _send_video_to_storage(file_path: str):
    if not file_path:
        return
    save_as_file_name = f"video_{round(time.time())}.mp4"
    file_upload.upload_file(save_as_file_name, file_path)


def _get_camera_functions(use_dummy_mode: bool):
    import camera_record_loop

    if use_dummy_mode:
        from camera_record_loop_dummy import prepare_camera, run_camera_loop

        return prepare_camera, run_camera_loop, camera_record_loop.shutdown_camera
    else:
        return camera_record_loop.prepare_camera, camera_record_loop.run_camera_loop, camera_record_loop.shutdown_camera


def main_loop(camera_id: int, use_dummy_mode: bool):
    print("Starting:", {"camera_id": camera_id, "use_dummy_mode": use_dummy_mode})
    prepare_camera, run_camera_loop, shutdown_camera = _get_camera_functions(use_dummy_mode)

    event_thread = Thread(target=_listen_camera_events, args=[camera_id], daemon=True)
    event_thread.start()

    _send_status(camera_id, CameraStatus.SYSTEM_STANDBY)
    _update_address_info(camera_id, SOCKET.socket_object)

    def _request_socket_update():
        SOCKET.socket_object = video_stream_producer.try_init_socket()  # noqa: F841
        _update_address_info(camera_id, SOCKET.socket_object)

    while True:

        if not _camera_on(camera_id):
            print("idle", {"camera_id": camera_id})
            time.sleep(2)
            continue

        _send_status(camera_id, CameraStatus.CAMERA_PREPARE)

        if not SOCKET.socket_object:
            _request_socket_update()

        video_capture = prepare_camera(camera_id)
        print("camera ready", {"camera_id": camera_id})
        _send_status(camera_id, CameraStatus.CAMERA_READY)

        record_info = run_camera_loop(
            video_capture,
            lambda: _camera_on(camera_id),
            lambda: _recording_on(camera_id),
            lambda status: _send_status(camera_id, status),
            lambda frame: _new_frame_received(SOCKET.socket_object, frame, _request_socket_update),
        )
        shutdown_camera(video_capture)

        _send_status(camera_id, CameraStatus.SYSTEM_STANDBY)

        if record_info.has_data:
            _send_video_to_storage(record_info.file_full_name)
        record_info.clean_up()


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main_loop(args.camera_id, args.use_dummy_mode)
