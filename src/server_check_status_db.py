import sqlite3 as sl

import config


def check_status_from_db(camera_id: int) -> bool:
    con = sl.connect(config.DB_NAME)

    with con:
        cursor = con.execute(
            "SELECT status FROM camera_status WHERE id = ? ORDER BY time DESC LIMIT 1", (str(camera_id))
        )
        camera = cursor.fetchone()
        return camera[0] if camera else None
