import time
from asyncio.queues import Queue
from dataclasses import dataclass

import cv2

from common_types import MemoryBufferImage
from server_check_status_db import check_status_from_db
from video_stream_consumer import receive_stream


@dataclass
class CameraConfig:
    route_id: int
    cameras: list[int]


camera_config = CameraConfig(1, [0, 1])


def check_status():
    while True:
        for camera_id in camera_config.cameras:
            status = check_status_from_db(camera_id)
            print("Camera status", {"camera_id": camera_id, "status": status})
            time.sleep(2.1)


async def get_video_streams_and_show_in_window(queue: Queue[MemoryBufferImage]):
    windows = {}
    for address, frame in receive_stream():
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        await queue.put(encodedImage)
        key = str(address)
        if key not in windows:
            windows[key] = True
            cv2.namedWindow(key)

        cv2.imshow(key, frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


async def get_video_streams(queue: Queue[MemoryBufferImage]):
    for address, frame in receive_stream():
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        await queue.put(encodedImage)
