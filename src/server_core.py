import time
from asyncio.queues import Queue
from dataclasses import dataclass

import cv2

from server_check_status_db import check_status_from_db
from video_stream_consumer import receive_stream


@dataclass
class SocketFramePayload:
    sender: str
    frame: str
    type: str = "frame"


@dataclass
class SocketStatusPayload:
    sender: str
    status: str
    type: str = "status"


SocketPayload = SocketStatusPayload | SocketFramePayload


@dataclass
class CameraConfig:
    route_id: int
    cameras: list[int]


camera_config = CameraConfig(1, [0, 1])


async def check_camera_status(queue: Queue[SocketStatusPayload]):
    while True:
        for camera_id in camera_config.cameras:
            status = check_status_from_db(camera_id)
            print("Camera status", {"camera_id": camera_id, "status": status})
            await queue.put(SocketStatusPayload(f"{camera_config.route_id}: {camera_id}", status))
        time.sleep(10)


# TODO: Add route/camera_id to queued message


async def get_video_streams_and_show_in_window(queue: Queue[SocketFramePayload]):
    windows = {}
    for address, frame in receive_stream():
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        await queue.put(SocketFramePayload(f"{address[0]}:{address[1]}", encodedImage.tobytes()))
        key = str(address)
        if key not in windows:
            windows[key] = True
            cv2.namedWindow(key)

        cv2.imshow(key, frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


async def get_video_streams(queue: Queue[SocketFramePayload]):
    for address, frame in receive_stream():
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        await queue.put(SocketFramePayload(f"{address[0]}:{address[1]}", encodedImage.tobytes()))
