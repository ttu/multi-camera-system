import os
import pathlib
import time
from asyncio.queues import Queue
from dataclasses import dataclass
from threading import Thread

import cv2
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from common_types import VideoFrame
from server_check_status_db import check_status_from_db
from server_toggle_start import set_camera_running
from video_stream_consumer import receive_stream

app = FastAPI()

current_path = str(pathlib.Path().resolve())
path_base = "" if current_path.endswith("src") else f"src{os.sep}"
PATH_STATIC = f"{path_base}templates"
app.mount("/site", StaticFiles(directory=PATH_STATIC, html=True), name="static")


@dataclass
class CameraConfig:
    route_id: int
    cameras: list[int]


camera_config = CameraConfig(1, [0, 1])
stream_queue: Queue[VideoFrame] = Queue()


def _check_status(camera_config: CameraConfig):
    while True:
        for camera_id in camera_config.cameras:
            status = check_status_from_db(camera_id)
            print("Camera status", {"camera_id": camera_id, "status": status})
            time.sleep(2.1)


def _get_video_streams_and_show_in_window():
    windows = {}
    for address, frame in receive_stream():
        stream_queue.put(frame)
        key = str(address)
        if key not in windows:
            windows[key] = True
            cv2.namedWindow(key)

        cv2.imshow(key, frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


def _get_video_streams():
    for address, frame in receive_stream():
        stream_queue.put(frame)


async def _get_frame():
    while True:
        next = await stream_queue.get()
        (flag, encodedImage) = cv2.imencode(".jpg", next)
        if flag:
            yield encodedImage


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
    check_thread = Thread(target=_check_status, args=[camera_config], daemon=True)
    check_thread.start()
    stream_thread = Thread(target=_get_video_streams_and_show_in_window, daemon=True)
    stream_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
