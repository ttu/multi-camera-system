import pickle
import socket
import struct

import config

PAYLOAD_SIZE = struct.calcsize("I")


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


def receive_stream():
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
                yield frame
