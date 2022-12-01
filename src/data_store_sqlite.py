import sqlite3

import common_config
from common_types import CameraStatus


def get_camera_recording(camera_id: int) -> bool | None:
    con = sqlite3.connect(common_config.DB_NAME)
    cursor = con.execute("SELECT recording FROM camera WHERE id = ?", (camera_id,))
    row = cursor.fetchone()
    return bool(row[0]) if row else None


def get_camera_running(camera_id: int) -> bool | None:
    con = sqlite3.connect(common_config.DB_NAME)
    cursor = con.execute("SELECT running FROM camera WHERE id = ?", (camera_id,))
    row = cursor.fetchone()
    return bool(row[0]) if row else None


def get_camera_status(camera_id: int) -> CameraStatus | None:
    con = sqlite3.connect(common_config.DB_NAME)
    cursor = con.execute("SELECT status FROM camera_status WHERE id = ? ORDER BY time DESC LIMIT 1", (str(camera_id)))
    row = cursor.fetchone()
    return CameraStatus(row[0]) if row else None


def get_camera_address(camera_id: int) -> str | None:
    con = sqlite3.connect(common_config.DB_NAME)
    cursor = con.execute("SELECT address FROM camera WHERE id = ?", (str(camera_id)))
    row = cursor.fetchone()
    return str(row[0]) if row else None


def update_camera_address(camera_id: int, address: str | None) -> bool:
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        cursor = con.execute("UPDATE camera SET address = ? WHERE id = ?", (address, camera_id))
        return cursor.rowcount > 0


def update_camera_recording(camera_id: int, recording: bool):
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        cursor = con.execute("UPDATE camera SET recording = ? WHERE id = ?", (recording, camera_id))
        return cursor.rowcount > 0


def update_camera_running(camera_id: int, running: bool) -> bool:
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        cursor = con.execute("UPDATE camera SET running = ? WHERE id = ?", (running, camera_id))
        return cursor.rowcount > 0


def update_camera_status(camera_id: int, status: CameraStatus) -> bool:
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        cursor = con.execute("INSERT INTO camera_status (id, status) VALUES (?,?)", (camera_id, status.name))
        return cursor.rowcount > 0


def toggle_camera_recording(camera_id: int) -> bool | None:
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT recording FROM camera WHERE id = ?", (str(camera_id)))
        row = cursor.fetchone()
        if not row:
            return None
        recording = bool(row[0])
        new_state = not recording
        cursor.execute("UPDATE camera SET recording = ? WHERE id = ?", (new_state, camera_id))
        return new_state if cursor.rowcount > 0 else None


def toggle_camera_running(camera_id: int) -> bool | None:
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT running FROM camera WHERE id = ?", (str(camera_id)))
        row = cursor.fetchone()
        if not row:
            return None
        running = bool(row[0])
        new_state = not running
        cursor.execute("UPDATE camera SET running = ? WHERE id = ?", (new_state, camera_id))
        return new_state if cursor.rowcount > 0 else None
