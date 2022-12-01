import sqlite3

import common_config


def create_db():
    con = sqlite3.connect(common_config.DB_NAME)
    with con:
        con.execute(
            """
            CREATE TABLE camera (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                running BOOLEAN DEFAULT FALSE,
                recording BOOLEAN DEFAULT FALSE,
                address TEXT DEFAULT NULL
            );
            """
        )
        con.execute(
            """
            CREATE TABLE camera_status (
                id INTEGER NOT NULL REFERENCES camera(id),
                status TEXT NOT NULL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id, status, time)
            );
            """
        )


def seed_db():
    con = sqlite3.connect(common_config.DB_NAME)

    sql = "INSERT INTO camera (id, name) values(?, ?)"
    data = [(0, "Main"), (1, "Upper A"), (2, "Lower B")]

    with con:
        cursor = con.executemany(sql, data)
        if cursor.rowcount == 0:
            print("Error")


create_db()
seed_db()
