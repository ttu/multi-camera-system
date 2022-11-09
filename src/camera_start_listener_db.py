import sqlite3 as sl

import config


def check_start_from_db(camera_id: int) -> bool:
    con = sl.connect(config.DB_NAME)

    with con:
        cursor = con.cursor()
        cursor.execute("SELECT running FROM camera WHERE id = ?", (camera_id,))
        camera = cursor.fetchone()
        running = bool(camera[0])
        return running
