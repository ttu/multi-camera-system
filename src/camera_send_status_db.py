import sqlite3 as sl

import common_config
from common_types import CameraStatus


def update_camera_status(camera_id: int, status: CameraStatus) -> None:
    con = sl.connect(common_config.DB_NAME)
    con.execute("INSERT INTO camera_status VALUES (?,?,CURRENT_TIMESTAMP)", (camera_id, status.name))
    con.commit()
    con.close()


def update_camera_address(camera_id: int, address: str) -> None:
    con = sl.connect(common_config.DB_NAME)
    con.execute("UPDATE camera SET address = ? WHERE id = ?", (address, camera_id))
    con.commit()
    con.close()
