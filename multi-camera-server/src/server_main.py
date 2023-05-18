import asyncio
import sys
from asyncio.queues import Queue
from dataclasses import asdict, dataclass
from threading import Thread

import uvicorn
from fastapi import FastAPI, Header, Request, Response, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

load_dotenv()

import common_config
import event_handler
import file_storage
import server_core
from common_types import CameraInfo, EventType, RouteInfo


app = FastAPI()

app.mount("/site", StaticFiles(directory=server_core.PATH_STATIC, html=True), name="static")

origins = ["http://localhost:8000", "localhost:8000"]


app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@dataclass
class CameraDto:
    cameraId: str
    name: str
    status: str
    frameCount: int


@dataclass
class RouteDto:
    routeId: int
    name: str
    cameras: list[CameraDto]


@dataclass
class RouteControlDto:
    routeId: str
    state: str


@dataclass
class CameraControlDto:
    cameraId: str
    state: str


@dataclass
class VideoFilesDto:
    files: list[str]


@dataclass
class SocketStatusDto:
    routeId: int
    cameraId: int
    status: str | None
    type: str = "status"


@dataclass
class RouteControlRequest:
    routeId: int
    state: str


@dataclass
class CameraControlRequest:
    camera_id: int
    state: str


status_queue: Queue[server_core.SocketStatusPayload] = Queue()
stream_queue: Queue[server_core.SocketFramePayload] = Queue()

status_sockets: list[WebSocket] = []
stream_sockets: dict[int, list[WebSocket]] = {}


async def _send_queue_messages_json(queue: Queue[server_core.SocketStatusPayload], sockets: list[WebSocket]):
    while True:
        next = await queue.get()
        for socket in sockets:
            try:
                dto = SocketStatusDto(next.route_id, next.camera_id, next.status)
                await socket.send_json(asdict(dto))
            except Exception as ex:
                sockets.remove(socket)
                print(ex)


async def _send_queue_messages_bytes(queue: Queue[server_core.SocketFramePayload], sockets: dict[str, list[WebSocket]]):
    while True:
        next = await queue.get()
        if not sockets or next.camera_id not in sockets:
            continue
        selected_sockets = sockets[next.camera_id]
        for socket in selected_sockets:
            try:
                await socket.send_bytes(next.frame)
            except Exception as ex:
                selected_sockets.remove(socket)
                print(ex)


def _map_camera_to_dto(camera: CameraInfo):
    return CameraDto(camera.camera_id, camera.name, camera.status or "unknown", 0)


def _map_route_info_to_dto(route: RouteInfo):
    cameras = [_map_camera_to_dto(c) for c in route.cameras]
    return RouteDto(route.route_id, route.name, cameras)


@app.get("/route-info/", response_model=list[RouteDto])
async def route_info(request: Request):
    route_data = [_map_route_info_to_dto(route) for route in server_core.ROUTE_INFOS]
    return route_data


@app.post("/control-route/", response_model=RouteControlDto)
async def control_route(request: Request):
    data = await request.json()
    route_id = data["routeId"]
    state = data["state"]

    if state not in ["start", "stop"]:
        return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)

    event = EventType.CAMERA_COMMAND_PREPARE if state == "start" else EventType.CAMERA_COMMAND_TURNOFF

    cameras = next(x.cameras for x in server_core.ROUTE_INFOS if x.route_id == route_id)

    for camera in cameras:
        _ = event_handler.send_event(event, camera.camera_id)
        print("Set state", {"camera_id": camera.camera_id, "state": event})

    return RouteControlDto(route_id, event.value)


@app.post("/control-camera/", response_model=CameraControlDto)
async def control_camera(request: Request):
    data = await request.json()
    camera_id = data["cameraId"]
    state = data["state"]
    event = EventType(state)

    if not server_core.has_camera(server_core.ROUTE_INFOS, int(camera_id)):
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)

    if not event:
        return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)

    _ = event_handler.send_event(event, camera_id)

    print("Set state", {"camera_id": camera_id, "state": event})
    return CameraControlDto(camera_id, event.value)


@app.get("/video-files/", response_model=VideoFilesDto)
async def get_video_files(request: Request):
    files = file_storage.get_files()
    if not files:
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
    return VideoFilesDto([f.name for f in files])


@app.get("/video/{video_id}")
async def download_video(video_id: str, range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    data, file_start, file_end, filesize = server_core.get_video_file_chunk(video_id, start, end)

    headers = {"Content-Range": f"bytes {file_start}-{file_end}/{filesize}", "Accept-Ranges": "bytes"}
    return Response(data, status_code=206, headers=headers, media_type="video/mp4")


# pylint: disable=unused-argument
@app.websocket("/camera-stream/{camera_id}")
async def websocket_stream_endpoint(websocket: WebSocket, camera_id: int):
    await websocket.accept()
    try:
        if camera_id not in stream_sockets:
            stream_sockets[camera_id] = []
        stream_sockets[camera_id].append(websocket)
        while True:
            await asyncio.sleep(100)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)
    stream_sockets[camera_id].remove(websocket)


@app.websocket("/status-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        status_sockets.append(websocket)
        while True:
            await asyncio.sleep(100)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)
    status_sockets.remove(websocket)


@app.on_event("startup")
async def startup_event():
    print("Server starting")

    await server_core.check_initial_camera_info(status_queue)

    asyncio.create_task(_send_queue_messages_json(status_queue, status_sockets))
    asyncio.create_task(_send_queue_messages_bytes(stream_queue, stream_sockets))
    asyncio.create_task(server_core.listen_for_server_events(status_queue))

    stream_thread = Thread(
        target=lambda queue: asyncio.run(server_core.get_video_streams(queue)), args=[stream_queue], daemon=True
    )
    stream_thread.start()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    uvicorn.run(app, host=common_config.UVICORN_HOST, port=common_config.UVICORN_PORT)
