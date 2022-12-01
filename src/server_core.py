import time
from asyncio.queues import Queue
from dataclasses import dataclass

import cv2

from data_store import get_camera_address, get_camera_status
from video_stream_consumer import receive_stream


@dataclass
class SocketFramePayload:
    sender: str
    frame: str
    type: str = "frame"


@dataclass
class SocketStatusPayload:
    sender: str
    status: str | None
    type: str = "status"


SocketPayload = SocketStatusPayload | SocketFramePayload


@dataclass
class CameraConfig:
    camera_id: int
    address: str | None = None


@dataclass
class RouteConfig:
    route_id: int
    cameras: list[CameraConfig]


route_config = RouteConfig(1, [CameraConfig(0), CameraConfig(1)])


async def check_camera_info(queue: Queue[SocketStatusPayload]):
    while True:
        for camera in route_config.cameras:
            camera_status = get_camera_status(camera.camera_id)
            status = camera_status.value if camera_status else None
            print("Camera status", {"camera_id": camera.camera_id, "status": status})
            await queue.put(SocketStatusPayload(f"{route_config.route_id}:{camera.camera_id}", status))

            address = get_camera_address(camera.camera_id)
            camera.address = address
            print("Camera address", {"camera_id": camera.camera_id, "address": address})

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
