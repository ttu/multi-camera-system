import asyncio
import dataclasses
import sys
from asyncio.queues import Queue
from threading import Thread

import uvicorn
from fastapi import FastAPI, Header, Request, Response, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

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


status_queue: Queue[server_core.SocketStatusPayload] = Queue()
stream_queue: Queue[server_core.SocketFramePayload] = Queue()

status_sockets: list[WebSocket] = []
stream_sockets: dict[str, list[WebSocket]] = {}


async def _send_queue_messages_json(queue: Queue[server_core.SocketStatusPayload], sockets: list[WebSocket]):
    while True:
        next = await queue.get()
        for socket in sockets:
            try:
                await socket.send_json(dataclasses.asdict(next))
            except Exception as ex:
                sockets.remove(socket)
                print(ex)


async def _send_queue_messages_bytes(queue: Queue[server_core.SocketFramePayload], sockets: dict[str, list[WebSocket]]):
    while True:
        next = await queue.get()
        if not sockets or str(next.sender) not in sockets:
            continue
        selected_sockets = sockets[str(next.sender)]
        for socket in selected_sockets:
            try:
                await socket.send_bytes(next.frame)
            except Exception as ex:
                selected_sockets.remove(socket)
                print(ex)


def _map_camera_to_dto(camera: CameraInfo):
    return {
        "cameraId": camera.camera_id,
        "name": camera.name,
        "status": camera.status,
        "frameCount": 0,
    }


def _map_route_info_to_dto(route: RouteInfo):
    cameras = {f"{route.route_id}:{c.camera_id}": _map_camera_to_dto(c) for c in route.cameras}
    return {"route_id": route.route_id, "name": route.name, "cameras": cameras}


@app.get("/camera-info/")
async def camera_info(request: Request):
    route_data = [_map_route_info_to_dto(route) for route in server_core.ROUTE_INFOS]
    return JSONResponse(content=route_data)


@app.post("/control-route/")
async def control_route(request: Request):
    data = await request.json()
    route_id = data["route_id"]
    state = data["state"]

    if state not in ["start", "stop"]:
        return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)

    event = EventType.CAMERA_COMMAND_PREPARE if state == "start" else EventType.CAMERA_COMMAND_TURNOFF

    cameras = next(x.cameras for x in server_core.ROUTE_INFOS if x.route_id == route_id)

    for camera in cameras:
        _ = event_handler.send_event(event, camera.camera_id)
        print("Set state", {"camera_id": camera.camera_id, "state": event})

    return JSONResponse(content={"route_id": route_id, "state": event.value})


@app.post("/control-camera/")
async def control_camera(request: Request):
    data = await request.json()
    camera_id = data["camera_id"]
    state = data["state"]
    event = EventType(state)

    if not server_core.has_camera(server_core.ROUTE_INFOS, int(camera_id)):
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)

    if not event:
        return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)

    _ = event_handler.send_event(event, camera_id)

    print("Set state", {"camera_id": camera_id, "state": event})
    return JSONResponse(content={"camera_id": camera_id, "state": event.value})


@app.get("/video-files/")
async def get_video_files(request: Request):
    files = file_storage.get_files()
    if not files:
        return Response(None, 500)
    return JSONResponse(content={"files": [f.name for f in files]})


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
            stream_sockets[str(camera_id)] = []
        stream_sockets[str(camera_id)].append(websocket)
        while True:
            await asyncio.sleep(100)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)
    stream_sockets[str(camera_id)].remove(websocket)


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

    uvicorn.run(app, host="127.0.0.1", port=8000)
