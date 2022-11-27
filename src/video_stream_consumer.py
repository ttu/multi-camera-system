import pickle
import socket
import struct
from queue import Queue
from threading import Thread
from typing import Generator, Tuple

import config
from camera_types import Address, VideoFrame

# https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b

PAYLOAD_SIZE = struct.calcsize("I")


def _is_frame(frame):
    return hasattr(frame, "size")


def _get_frame_data(conn: socket.socket, data: bytes) -> Tuple[bytes, bytes]:
    try:
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
    except ConnectionResetError:
        return None, None


def _on_new_client(client_socket: socket.socket, address: Address, queue: Queue[Tuple[Address, VideoFrame]]):
    data = b""
    with client_socket:
        print(f"Connected by {address}")
        while True:
            data, frame_data = _get_frame_data(client_socket, data)
            if not frame_data or frame_data == b"":
                continue
            frame = pickle.loads(frame_data)
            if _is_frame(frame):
                queue.put((address, frame))


def _start_socket_listener(queue: Queue[Tuple[Address, VideoFrame]]) -> Generator[VideoFrame, None, None]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.SERVER_HOST, config.SERVER_PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            Thread(target=_on_new_client, args=[conn, addr, queue], daemon=True).start()


def receive_stream() -> Generator[Tuple[Address, VideoFrame], None, None]:
    queue: Queue[Tuple[Address, VideoFrame]] = Queue()
    listen_thread = Thread(target=_start_socket_listener, args=[queue], daemon=True)
    listen_thread.start()

    while True:
        address, data = queue.get(True, None)
        yield address, data
