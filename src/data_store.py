import psycopg

import common_config
from common_types import CameraStatus

# pylint: disable=not-context-manager


def get_camera_recording(camera_id: int) -> bool | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT recording FROM camera WHERE id = %s", (camera_id,))
            row = cur.fetchone()
            return bool(row[0]) if row else None


def get_camera_running(camera_id: int) -> bool | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT running FROM camera WHERE id = %s", (camera_id,))
            row = cur.fetchone()
            return bool(row[0]) if row else None


def get_camera_status(camera_id: int) -> CameraStatus | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT status FROM camera_status WHERE id = %s ORDER BY time DESC LIMIT 1", (camera_id,))
            row = cur.fetchone()
            return CameraStatus(row[0]) if row else None


def get_camera_address(camera_id: int) -> str | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT address FROM camera WHERE id = %s", (camera_id,))
            row = cur.fetchone()
            return str(row[0]) if row else None


def update_camera_address(camera_id: int, address: str | None) -> bool:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE camera SET address = %s WHERE id = %s", (address, camera_id))
            return cur.rowcount > 0


def update_camera_recording(camera_id: int, recording: bool):
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE camera SET recording = %s WHERE id = %s", (recording, camera_id))
            return cur.rowcount > 0


def update_camera_running(camera_id: int, running: bool) -> bool:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE camera SET running = %s WHERE id = %s", (running, camera_id))
            return cur.rowcount > 0


def update_camera_status(camera_id: int, status: CameraStatus) -> bool:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO camera_status (id, status) VALUES (%s,%s)", (camera_id, status.name))
            return cur.rowcount > 0


def toggle_camera_recording(camera_id: int) -> bool | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT recording FROM camera WHERE id = %s", (camera_id,))
            row = cur.fetchone()
            if not row:
                return None
            recording = bool(row[0])
            new_state = not recording
            cur.execute("UPDATE camera SET recording = %s WHERE id = %s", (new_state, camera_id))
            return new_state if cur.rowcount > 0 else None


def toggle_camera_running(camera_id: int) -> bool | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT running FROM camera WHERE id = %s", (camera_id,))
            row = cur.fetchone()
            if not row:
                return None
            running = bool(row[0])
            new_state = not running
            cur.execute("UPDATE camera SET running = %s WHERE id = %s", (new_state, camera_id))
            return new_state if cur.rowcount > 0 else None
