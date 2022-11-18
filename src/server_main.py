import pickle
import socket
import struct
import time
from dataclasses import dataclass
from threading import Thread

import cv2

import config
from server_check_status_db import check_status_from_db
from server_toggle_start import set_camera_running

PAYLOAD_SIZE = struct.calcsize("I")


@dataclass
class CameraConfig:
    route_id: int
    cameras: list[int]


c = CameraConfig(1, [0, 1])


def _check_status(camera_config: CameraConfig):
    while True:
        for c in camera_config.cameras:
            status = check_status_from_db(c)
            print("Camera status", {"camera_id": c, "status": status})
            time.sleep(2.1)


# https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
def _get_frame_data(conn, data):
    while len(data) < PAYLOAD_SIZE:
        data += conn.recv(4096)
    packed_msg_size = data[:PAYLOAD_SIZE]
    data = data[PAYLOAD_SIZE:]
    msg_size = struct.unpack("I", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    return data, frame_data


def _receive_stream():
    data = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.SERVER_HOST, config.SERVER_PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data, frame_data = _get_frame_data(conn, data)
                if frame_data == "":
                    break
                frame = pickle.loads(frame_data)
                cv2.imshow("server", frame)
                cv2.waitKey(1)

    cv2.destroyAllWindows()


def main_loop():
    print("Server starting")
    check_thread = Thread(target=_check_status, args=[c], daemon=True)
    check_thread.start()
    stream_thread = Thread(target=_receive_stream, daemon=True)
    stream_thread.start()

    # TODO: Receive start signal from API
    set_camera_running(0, True)

    while True:
        print("Server waiting")

        time.sleep(2)


if __name__ == "__main__":
    main_loop()
