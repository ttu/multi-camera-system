import sqlite3 as sl
import sys

import config


def set_camera_running(camera_id: int, running: bool):
    con = sl.connect(config.DB_NAME)
    with con:
        con.execute("UPDATE camera SET running = ? WHERE id = ?", (running, camera_id))
        print("Set state", {"camera_id": camera_id, "running": running})


def toggle_start(camera_id: int):
    con = sl.connect(config.DB_NAME)
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT running FROM camera WHERE id = ?", (camera_id,))
        camera = cursor.fetchone()
        running = bool(camera[0])
        cursor.execute("UPDATE camera SET running = ? WHERE id = ?", (not running, camera_id))
        print("Set state", {"camera_id": camera_id, "running": not running})


if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else 0
    toggle_start(id)
