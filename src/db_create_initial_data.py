import psycopg

import common_config


def create_db():
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE camera (
                    id INTEGER NOT NULL PRIMARY KEY,
                    name TEXT,
                    running BOOLEAN DEFAULT FALSE,
                    recording BOOLEAN DEFAULT FALSE,
                    address TEXT DEFAULT NULL
                );
                """
            )
            cur.execute(
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
    sql = "INSERT INTO camera (id, name) values(%s, %s)"
    data = [(0, "Main"), (1, "Upper A"), (2, "Lower B")]

    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, data)
            if cur.rowcount == 0:
                print("Error")


create_db()
seed_db()
