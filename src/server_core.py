from asyncio.queues import Queue
from dataclasses import dataclass

import cv2

import data_store
import event_handler
import video_stream_consumer
from common_types import EventType, RouteInfo


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

route_info = RouteInfo(1, [])
# TODO: Add route to DB
route_1_cameras = [0, 1]


async def listen_for_server_events(queue: Queue[SocketStatusPayload]):
    async for event, (camera_id, payload) in event_handler.wait_for_events_async(
        [EventType.CAMERA_UPDATE_ADDRESS, EventType.CAMERA_UPDATE_STATUS]
    ):
        if event == EventType.CAMERA_UPDATE_ADDRESS.value:
            camera = [camera for camera in route_info.cameras if camera.camera_id == int(camera_id)][0]
            camera.address = payload
            print("Camera address", {"camera_id": camera.camera_id, "address": payload})
        elif event == EventType.CAMERA_UPDATE_STATUS.value:
            await queue.put(SocketStatusPayload(f"{route_info.route_id}:{camera_id}", payload))
            print("Camera status", {"camera_id": camera_id, "status": payload})


async def check_initial_camera_info(queue: Queue[SocketStatusPayload]):
    for camera_id in route_1_cameras:
        camera = data_store.get_camera_info(camera_id)
        if not camera:
            continue

        route_info.cameras.append(camera)
        print("Camera address", {"camera_id": camera.camera_id, "address": camera.address})
        print("Camera status", {"camera_id": camera.camera_id, "status": camera.status})
        await queue.put(SocketStatusPayload(f"{route_info.route_id}:{camera.camera_id}", camera.status))


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
        camera = [c for c in route_info.cameras if c.address == key]
        if camera:
            await queue.put(SocketFramePayload(str(camera[0].camera_id), encodedImage.tobytes()))
