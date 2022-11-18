import pickle
import socket
import struct
import time
from dataclasses import dataclass
from threading import Thread

import cv2

import config
from server_check_status_db import check_status_from_db


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


def _receive_stream():
    # https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
    payload_size = struct.calcsize("I")
    data = b""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.SERVER_HOST, config.SERVER_PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                while len(data) < payload_size:
                    data += conn.recv(4096)
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("I", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                if frame_data == "":
                    break
                frame = pickle.loads(frame_data)
                cv2.imshow("server", frame)
                cv2.waitKey(1)

    cv2.destroyAllWindows()


def main_loop():
    print("Server starting")
    check_thread = Thread(target=_check_status, args=[c])
    check_thread.start()
    _stream_thread = Thread(target=_receive_stream)
    _stream_thread.start()

    while True:
        print("Server waiting")
        time.sleep(2)


if __name__ == "__main__":
    main_loop()
