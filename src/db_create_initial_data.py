import sqlite3 as sl

import common_config

con = sl.connect(common_config.DB_NAME)


def create_db():
    with con:
        con.execute(
            """
            CREATE TABLE camera (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                running BOOLEAN,
                recording BOOLEAN
            );
            """
        )
        con.execute(
            """
            CREATE TABLE camera_status (
                id INTEGER NOT NULL REFERENCES camera(id),
                status TEXT NOT NULL,
                time TIMESTAMP,
                PRIMARY KEY(id, status, time)
            );
            """
        )


def seed_db():
    sql = "INSERT INTO camera (id, name, running, recording) values(?, ?, ?, ?)"
    data = [(0, "Main", False, False), (1, "Upper A", False, False), (2, "Lower B", False, False)]

    with con:
        con.executemany(sql, data)


create_db()
seed_db()
