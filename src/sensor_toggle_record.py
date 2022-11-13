import sqlite3 as sl

import config

UPDATE_STATEMEMT = "UPDATE camera SET recording = ? WHERE id = ?"


def set_recording(camera_id: int, recording: bool):
    con = sl.connect(config.DB_NAME)
    con.execute(UPDATE_STATEMEMT, (not recording, camera_id))
    print("Set state", {"camera_id": camera_id, "recording": not recording})


def toggle_record(camera_id: int):
    con = sl.connect(config.DB_NAME)

    with con:
        cursor = con.cursor()
        cursor.execute("SELECT recording FROM camera WHERE id = ?", (camera_id,))
        camera = cursor.fetchone()
        recording = bool(camera[0])
        cursor.execute(UPDATE_STATEMEMT, (not recording, camera_id))
        print("Set state", {"camera_id": camera_id, "recording": not recording})


toggle_record(0)
