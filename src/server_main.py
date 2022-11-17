import time
from dataclasses import dataclass
from threading import Thread

from server_check_status_db import check_status_from_db


@dataclass
class Config:
    route_id: int
    cameras: list[int]


c = Config(1, [0, 1])


def _check_status(config: Config):
    while True:
        for c in config.cameras:
            status = check_status_from_db(c)
            print("Camera status", {"camera_id": c, "status": status})
            time.sleep(2.1)


def main_loop():
    print("Server starting")
    check_thread = Thread(target=_check_status, args=[c])
    check_thread.start()

    while True:
        print("Server waiting")
        time.sleep(2)


if __name__ == "__main__":
    main_loop()
