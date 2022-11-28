import sqlite3 as sl

import common_config


def check_recording_from_db(camera_id: int) -> bool:
    con = sl.connect(common_config.DB_NAME)

    with con:
        cursor = con.cursor()
        cursor.execute("SELECT recording FROM camera WHERE id = ?", (camera_id,))
        camera = cursor.fetchone()
        recording = bool(camera[0])
        return recording
