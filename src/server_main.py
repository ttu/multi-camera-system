import asyncio
import dataclasses
import os
import pathlib
import sys
from asyncio.queues import Queue
from threading import Thread

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import event_handler
import server_core
from common_types import CameraInfo, EventType, RouteInfo

app = FastAPI()

current_path = str(pathlib.Path().resolve())
path_base = "" if current_path.endswith("src") else f"src{os.sep}"
PATH_STATIC = f"{path_base}templates"
app.mount("/site", StaticFiles(directory=PATH_STATIC, html=True), name="static")


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
    return {f"{route.route_id}:{c.camera_id}": _map_camera_to_dto(c) for c in route.cameras}


@app.get("/camera-info/")
async def camera_info(request: Request):
    camera_data = _map_route_info_to_dto(server_core.route_info)
    return JSONResponse(content=camera_data)


@app.post("/control-camera/")
async def control_camera(request: Request):
    data = await request.json()
    camera_id = data["camera_id"]
    state = data["state"]
    event = EventType(state)

    # TODO: Validate camera_id
    if not event:
        return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)

    _ = event_handler.send_event(event, camera_id)

    print("Set state", {"camera_id": camera_id, "state": event})
    return JSONResponse(content={"camera_id": camera_id, "state": event.value})


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
