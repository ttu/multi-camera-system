import psycopg

import common_config

from common_types import CameraInfo, CameraStatus, RouteInfo


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


def get_routes() -> list[RouteInfo]:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT r.id, r.name, c.cameras FROM route r
                LEFT JOIN (SELECT route_id, array_agg(camera_id) as cameras FROM route_cameras GROUP BY route_id) c
                ON r.id = c.route_id
                """
            )
            rows = cur.fetchall()
            # TODO: Fetch cameras with routes query
            return [
                RouteInfo(
                    row[0], row[1], [x for x in [get_camera_info(camera_id) for camera_id in row[2]] if x is not None]
                )
                for row in rows
            ]


def get_camera_info(camera_id: int) -> CameraInfo | None:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ca.id, ca.name, ca.address, cs.status, cs.status_update_time FROM camera ca
                LEFT JOIN (
                    SELECT id, status, time as status_update_time
                    FROM camera_status
                    WHERE id = %(camera_id)s
                    ORDER BY time DESC LIMIT 1
                ) cs
                ON ca.id = cs.id
                WHERE ca.id = %(camera_id)s
                """,
                ({"camera_id": camera_id}),
            )
            row = cur.fetchone()
            return CameraInfo(row[0], row[1], row[2], None, row[3], row[4]) if row else None


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
