from enum import Enum
from typing import Any

VideoWriter = Any  # cv2.VideoWriter
VideoCaptureDevice = Any  # cv2.VideoCapture


class CameraStatus(Enum):
    ON = "ON"
    OFF = "OFF"
    READY = "READY"
    RECORDING = "RECORDING"
