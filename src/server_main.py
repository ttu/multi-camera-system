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

from server_core import SocketFramePayload, SocketPayload, SocketStatusPayload, check_camera_info, get_video_streams
from server_toggle_start import set_camera_running

app = FastAPI()

current_path = str(pathlib.Path().resolve())
path_base = "" if current_path.endswith("src") else f"src{os.sep}"
PATH_STATIC = f"{path_base}templates"
app.mount("/site", StaticFiles(directory=PATH_STATIC, html=True), name="static")


status_queue: Queue[SocketStatusPayload] = Queue()
stream_queue: Queue[SocketFramePayload] = Queue()


async def _get_message_from_queue(queue: Queue[SocketPayload]):
    while True:
        next = await queue.get()
        yield next


@app.post("/control-camera/")
async def start_camera(request: Request):
    data = await request.json()
    if data["camera_id"] != 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

    set_camera_running(data["camera_id"], data["state"])
    return JSONResponse(content={"camera_id": data["camera_id"], "state": data["state"]})


@app.websocket("/camera-stream/{camera_id}")
async def websocket_stream_endpoint(websocket: WebSocket, camera_id: int):
    await websocket.accept()
    try:
        async for message in _get_message_from_queue(stream_queue):
            await websocket.send_bytes(message.frame)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)


@app.websocket("/status-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for message in _get_message_from_queue(status_queue):
            await websocket.send_json(dataclasses.asdict(message))
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)


@app.on_event("startup")
async def startup_event():
    print("Server starting")
    check_thread = Thread(target=lambda queue: asyncio.run(check_camera_info(queue)), args=[status_queue], daemon=True)
    check_thread.start()
    stream_thread = Thread(target=lambda queue: asyncio.run(get_video_streams(queue)), args=[stream_queue], daemon=True)
    stream_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
