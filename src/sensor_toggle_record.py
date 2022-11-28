import sqlite3 as sl
import sys

import common_config

UPDATE_STATEMEMT = "UPDATE camera SET recording = ? WHERE id = ?"


def set_recording(camera_id: int, recording: bool):
    con = sl.connect(common_config.DB_NAME)
    con.execute(UPDATE_STATEMEMT, (not recording, camera_id))
    print("Set state", {"camera_id": camera_id, "recording": not recording})


def toggle_record(camera_id: int):
    con = sl.connect(common_config.DB_NAME)

    with con:
        cursor = con.cursor()
        cursor.execute("SELECT recording FROM camera WHERE id = ?", (camera_id,))
        camera = cursor.fetchone()
        recording = bool(camera[0])
        cursor.execute(UPDATE_STATEMEMT, (not recording, camera_id))
        print("Set state", {"camera_id": camera_id, "recording": not recording})


if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else 0
    toggle_record(id)
