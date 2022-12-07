import time
from asyncio.queues import Queue
from dataclasses import dataclass

import cv2

import data_store
import event_handler
import video_stream_consumer
from common_types import EventType


@dataclass
class SocketFramePayload:
    sender: str
    frame: bytes
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


async def listen_for_server_events():
    async for _, (camera_id, address) in event_handler.wait_for_events_async([EventType.CAMERA_ADDRESS_UPDATE]):
        camera = [camera for camera in route_config.cameras if camera.camera_id == int(camera_id)][0]
        camera.address = address
        print("Camera address", {"camera_id": camera.camera_id, "address": address})


async def check_camera_info(queue: Queue[SocketStatusPayload]):
    while True:
        for camera in route_config.cameras:
            camera_status = data_store.get_camera_status(camera.camera_id)
            status = camera_status.value if camera_status else None
            print("Camera status", {"camera_id": camera.camera_id, "status": status})
            await queue.put(SocketStatusPayload(f"{route_config.route_id}:{camera.camera_id}", status))

            # address = data_store.get_camera_address(camera.camera_id)
            # camera.address = address
            # print("Camera address", {"camera_id": camera.camera_id, "address": address})

        time.sleep(3)


# TODO: Add route/camera_id to queued message


async def get_video_streams_and_show_in_window(queue: Queue[SocketFramePayload]):
    windows = {}
    for address, frame in video_stream_consumer.receive_stream():
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
    for address, frame in video_stream_consumer.receive_stream():
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        key = f"{address[0]}:{address[1]}"
        camera = [c for c in route_config.cameras if c.address == key]
        if camera:
            await queue.put(SocketFramePayload(camera[0].camera_id, encodedImage.tobytes()))
