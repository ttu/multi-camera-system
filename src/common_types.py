from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple

VideoCaptureDevice = Any  # cv2.VideoCapture
VideoFrame = Any
MemoryBufferImage = Any

# https://docs.python.org/3/library/socket.html#socket-families
Address = Tuple[str, int]  # socket _RetAddress

RecordedVideoInfo = str


class VideoWriter:
    def __init__(self, output):
        self.output = output
        self.has_data = False

    def write(self, data):
        self.has_data = True
        self.output.write(data)

    def release(self):
        self.output.release()


@dataclass
class CameraInfo:
    camera_id: int
    address: str | None = None
    address_update_time: str | None = None
    status: str | None = None
    status_update_time: str | None = None


@dataclass
class RouteInfo:
    route_id: int
    cameras: list[CameraInfo]


class CameraStatus(Enum):
    SYSTEM_STANDBY = "SYSTEM_STANDBY"
    SYSTEM_OFF = "SYSTEM_OFF"
    CAMERA_PREPARE = "CAMERA_PREPARE"
    CAMERA_READY = "CAMERA_READY"
    CAMERA_RECORDING = "CAMERA_RECORDING"


class EventType(Enum):
    CAMERA_COMMAND_PREPARE = "CAMERA_COMMAND_PREPARE"
    CAMERA_COMMAND_RECORD = "CAMERA_COMMAND_RECORD"
    CAMERA_COMMAND_STOP_RECORD = "CAMERA_COMMAND_STOP_RECORD"
    CAMERA_COMMAND_TURNOFF = "CAMERA_COMMAND_TURNOFF"
    CAMERA_UPDATE_ADDRESS = "CAMERA_UPDATE_ADDRESS"
    CAMERA_UPDATE_STATUS = "CAMERA_UPDATE_STATUS"
