import sqlite3 as sl

import config


def toggle_start(camera_id: int):
    con = sl.connect(config.DB_NAME)

    with con:
        cursor = con.cursor()
        cursor.execute("SELECT running FROM camera WHERE id = ?", (camera_id,))
        camera = cursor.fetchone()
        running = bool(camera[0])
        cursor.execute("UPDATE camera SET running = ? WHERE id = ?", (not running, camera_id))
        print("Set state", {"camera_id": camera_id, "running": not running})


toggle_start(0)
