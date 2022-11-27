import os
import pathlib
import time
from dataclasses import dataclass
from queue import Queue
from threading import Thread

import cv2
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from camera_types import VideoFrame
from server_check_status_db import check_status_from_db
from server_toggle_start import set_camera_running
from video_stream_consumer import receive_stream

app = FastAPI()

current_path = str(pathlib.Path().resolve())
PATH = "templates" if current_path.endswith("src") else f"src{os.sep}templates"
templates = Jinja2Templates(directory=PATH)


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


def _get_frame():
    while True:
        next = stream_queue.get(True)
        (flag, encodedImage) = cv2.imencode(".jpg", next)
        if flag:
            yield encodedImage


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        for frame in _get_frame():
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

    # TODO: Receive start signal from API
    set_camera_running(0, True)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
