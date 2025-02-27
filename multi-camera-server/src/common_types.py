from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Tuple


VideoFrame = Any
MemoryBufferImage = Any

# https://docs.python.org/3/library/socket.html#socket-families
Address = Tuple[str, int]  # socket _RetAddress


class VideoWriter:
    def __init__(self, output, file_full_name):
        self.output = output
        self.has_data = False
        self.file_full_name = file_full_name

    def write(self, data):
        self.has_data = True
        self.output.write(data)

    def release(self):
        self.output.release()


class ViderRecording:
    def __init__(self, has_data, file_full_name):
        self.has_data = has_data
        self.file_full_name = file_full_name

    def clean_up(self):
        if Path(self.file_full_name).exists():
            Path(self.file_full_name).unlink()


class VideoCaptureDevice:
    def __init__(self, camera_id: int, get_frame: Callable[[], Tuple[Any, VideoFrame]], release: Callable[[], None]):
        self.camera_id = camera_id
        self.get_frame = get_frame
        self.release = release


@dataclass
class CameraConfig:
    camera_id: int
    resolution: Tuple[int, int]


@dataclass
class CameraInfo:
    camera_id: int
    name: str
    address: str | None = None
    address_update_time: str | None = None
    status: str | None = None
    status_update_time: str | None = None


@dataclass
class RouteInfo:
    route_id: int
    name: str
    cameras: list[CameraInfo]


@dataclass
class FileInfo:
    name: str
    size: int


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
