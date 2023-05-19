import pickle
import socket
import struct

import common_config
from common_types import VideoFrame


def try_init_socket() -> socket.socket | None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = (
            common_config.SERVER_HOST
            if common_config.IS_SERVER_HOST_IP
            else socket.gethostbyname(common_config.SERVER_HOST)
        )
        s.connect((ip, common_config.SERVER_PORT))
        return s
    except Exception:
        print("Socket init failed")
        return None


def send_frame(s: socket.socket, frame: VideoFrame) -> bool:
    x_as_bytes = pickle.dumps(frame)
    size = len(x_as_bytes)
    p = struct.pack("I", size)
    data_to_send = p + x_as_bytes
    try:
        s.sendall(data_to_send)
        return True
    except Exception:
        print("Socket is out")
        return False
