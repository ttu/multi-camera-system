import pickle
import socket
import struct

import common_config
from common_types import VideoFrame


def try_init_socket() -> socket.socket | None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((common_config.SERVER_HOST, common_config.SERVER_PORT))
        return s
    except Exception:
        print("Socket init failed")
        return None


def send_frame(socket: socket.socket, frame: VideoFrame):
    x_as_bytes = pickle.dumps(frame)
    size = len(x_as_bytes)
    p = struct.pack("I", size)
    data_to_send = p + x_as_bytes
    socket.sendall(data_to_send)
