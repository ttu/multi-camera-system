import asyncio
import dataclasses
import os
import pathlib
from asyncio.queues import Queue
from threading import Thread

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import event_handler
from common_types import EventType
from server_core import SocketFramePayload, SocketStatusPayload, check_camera_info, get_video_streams

app = FastAPI()

current_path = str(pathlib.Path().resolve())
path_base = "" if current_path.endswith("src") else f"src{os.sep}"
PATH_STATIC = f"{path_base}templates"
app.mount("/site", StaticFiles(directory=PATH_STATIC, html=True), name="static")


status_queue: Queue[SocketStatusPayload] = Queue()
stream_queue: Queue[SocketFramePayload] = Queue()

status_sockets: list[WebSocket] = []
stream_sockets: list[WebSocket] = []


async def _send_queue_messages_json(queue: Queue[SocketStatusPayload], sockets: list[WebSocket]):
    while True:
        next = await queue.get()
        for socket in sockets:
            await socket.send_json(dataclasses.asdict(next))


async def _send_queue_messages_bytes(queue: Queue[SocketFramePayload], sockets: list[WebSocket]):
    while True:
        next = await queue.get()
        for socket in sockets:
            await socket.send_bytes(next.frame)


@app.post("/control-camera/")
async def start_camera(request: Request):
    data = await request.json()
    camera_id = data["camera_id"]
    state = data["state"]
    event = EventType(state)

    if data["camera_id"] != 0 or not event:
        return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)

    _ = event_handler.send_event(event, camera_id)

    print("Set state", {"camera_id": camera_id, "state": event})
    return JSONResponse(content={"camera_id": camera_id, "state": event.value})


# pylint: disable=unused-argument
@app.websocket("/camera-stream/{camera_id}")
async def websocket_stream_endpoint(websocket: WebSocket, camera_id: int):
    await websocket.accept()
    try:
        stream_sockets.append(websocket)
        while True:
            await asyncio.sleep(100)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)
    stream_sockets.remove(websocket)


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

    asyncio.create_task(_send_queue_messages_json(status_queue, status_sockets))
    asyncio.create_task(_send_queue_messages_bytes(stream_queue, stream_sockets))

    check_thread = Thread(target=lambda queue: asyncio.run(check_camera_info(queue)), args=[status_queue], daemon=True)
    check_thread.start()
    stream_thread = Thread(target=lambda queue: asyncio.run(get_video_streams(queue)), args=[stream_queue], daemon=True)
    stream_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
