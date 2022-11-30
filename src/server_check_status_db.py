import sqlite3 as sl

import common_config


def check_status_from_db(camera_id: int) -> bool:
    con = sl.connect(common_config.DB_NAME)

    with con:
        cursor = con.execute(
            "SELECT status FROM camera_status WHERE id = ? ORDER BY time DESC LIMIT 1", (str(camera_id))
        )
        row = cursor.fetchone()
        return row[0] if row else None


def check_camera_address_from_db(camera_id: int) -> bool:
    con = sl.connect(common_config.DB_NAME)

    with con:
        cursor = con.execute("SELECT address FROM camera WHERE id = ?", (str(camera_id)))
        row = cursor.fetchone()
        return row[0] if row else None
