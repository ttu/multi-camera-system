from asyncio.queues import Queue
from dataclasses import dataclass

import cv2

import data_store
import event_handler
import video_stream_consumer
from common_types import CameraInfo, EventType, RouteInfo


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


ROUTE_INFOS: list[RouteInfo] = []


def _get_route_for_camera(routes: list[RouteInfo], camera_id: int) -> RouteInfo:
    routes = [r for r in routes if camera_id in [c.camera_id for c in r.cameras]]
    if not routes:
        raise Exception("Not found")
    return routes[0]


def _get_camera(routes: list[RouteInfo], camera_id: int) -> CameraInfo:
    all_cameras: list[CameraInfo] = sum([r.cameras for r in routes], [])
    cameras = [camera for camera in all_cameras if camera.camera_id == int(camera_id)]
    if not cameras:
        raise Exception("Not found")
    return cameras[0]


def _get_camera_with_address(routes: list[RouteInfo], address: str) -> CameraInfo:
    all_cameras: list[CameraInfo] = sum([r.cameras for r in routes], [])
    cameras = [camera for camera in all_cameras if camera.address == address]
    if not cameras:
        raise Exception("Not found")
    return cameras[0]


async def listen_for_server_events(queue: Queue[SocketStatusPayload]):
    async for event, (camera_id, payload) in event_handler.wait_for_events_async(
        [EventType.CAMERA_UPDATE_ADDRESS, EventType.CAMERA_UPDATE_STATUS]
    ):
        if event == EventType.CAMERA_UPDATE_ADDRESS.value:
            camera = _get_camera(ROUTE_INFOS, int(camera_id))
            camera.address = payload
            print("Camera address", {"camera_id": camera.camera_id, "address": payload})
        elif event == EventType.CAMERA_UPDATE_STATUS.value:
            route = _get_route_for_camera(ROUTE_INFOS, int(camera_id))
            await queue.put(SocketStatusPayload(f"{route.route_id}:{camera_id}", payload))
            print("Camera status", {"camera_id": camera_id, "status": payload})


async def check_initial_camera_info(queue: Queue[SocketStatusPayload]):
    routes = data_store.get_routes()
    ROUTE_INFOS.extend(routes)

    for route in ROUTE_INFOS:
        for camera in route.cameras:
            print("Camera address", {"camera_id": camera.camera_id, "address": camera.address})
            print("Camera status", {"camera_id": camera.camera_id, "status": camera.status})
            await queue.put(SocketStatusPayload(f"{route.route_id}:{camera.camera_id}", camera.status))


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
        camera = _get_camera_with_address(ROUTE_INFOS, key)
        await queue.put(SocketFramePayload(str(camera.camera_id), encodedImage.tobytes()))
