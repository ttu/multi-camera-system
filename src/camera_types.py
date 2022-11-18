from enum import Enum
from typing import Any

VideoWriter = Any  # cv2.VideoWriter
VideoCaptureDevice = Any  # cv2.VideoCapture
VideoFrame = Any


class CameraStatus(Enum):
    SYSTEM_STANDBY = "SYSTEM_STANDBY"
    SYSTEM_OFF = "SYSTEM_OFF"
    CAMERA_READY = "CAMERA_READY"
    CAMERA_RECORDING = "CAMERA_RECORDING"
