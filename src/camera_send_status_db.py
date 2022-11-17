import sqlite3 as sl

import config
from camera_types import CameraStatus


def update_camera_status(camera_id: int, status: CameraStatus) -> None:
    con = sl.connect(config.DB_NAME)
    con.execute("INSERT INTO camera_status VALUES (?,?,CURRENT_TIMESTAMP)", (camera_id, status.name))
    con.commit()
    con.close()
