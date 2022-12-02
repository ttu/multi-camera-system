from enum import Enum
from typing import Any, Tuple

VideoWriter = Any  # cv2.VideoWriter
VideoCaptureDevice = Any  # cv2.VideoCapture
VideoFrame = Any
MemoryBufferImage = Any

# https://docs.python.org/3/library/socket.html#socket-families
Address = Tuple[str, int]  # socket _RetAddress


class CameraStatus(Enum):
    SYSTEM_STANDBY = "SYSTEM_STANDBY"
    SYSTEM_OFF = "SYSTEM_OFF"
    CAMERA_PREPARE = "CAMERA_PREPARE"
    CAMERA_READY = "CAMERA_READY"
    CAMERA_RECORDING = "CAMERA_RECORDING"


class EventType(Enum):
    CAMERA_PREPARE = "CAMERA_PREPARE"
    CAMERA_RECORD = "CAMERA_RECORD"
    CAMERA_STOP_RECORD = "CAMERA_STOP_RECORD"
    CAMERA_TURNOFF = "CAMERA_TURNOFF"
    CAMERA_ADDRESS_UPDATE = "CAMERA_ADDRESS_UPDATE"
    CAMERA_STATUS_UPDATE = "CAMERA_STATUS_UPDATE"
