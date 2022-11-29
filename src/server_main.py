import asyncio
import os
import pathlib
from asyncio.queues import Queue
from threading import Thread

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from common_types import MemoryBufferImage
from server_core import check_status, get_video_streams
from server_toggle_start import set_camera_running

app = FastAPI()

current_path = str(pathlib.Path().resolve())
path_base = "" if current_path.endswith("src") else f"src{os.sep}"
PATH_STATIC = f"{path_base}templates"
app.mount("/site", StaticFiles(directory=PATH_STATIC, html=True), name="static")


stream_queue: Queue[MemoryBufferImage] = Queue()


async def _get_frame():
    while True:
        next = await stream_queue.get()
        yield next


@app.post("/start-camera/")
async def start_camera(request: Request):
    data = await request.json()
    if data["camera_id"] != 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

    set_camera_running(data["camera_id"], True)
    return JSONResponse(content={"camera_id": data["camera_id"], "running": True})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for frame in _get_frame():
            await websocket.send_bytes(frame.tobytes())
    except WebSocketDisconnect:
        print("Client disconnected")


@app.on_event("startup")
async def startup_event():
    print("Server starting")
    check_thread = Thread(target=check_status, daemon=True)
    check_thread.start()
    stream_thread = Thread(target=lambda queue: asyncio.run(get_video_streams(queue)), args=[stream_queue], daemon=True)
    stream_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
