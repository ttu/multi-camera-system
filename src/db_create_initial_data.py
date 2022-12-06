import psycopg

import common_config

# pylint: disable=not-context-manager


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
            cur.execute(
                """
                CREATE TABLE camera_event (
                    id SERIAL PRIMARY KEY,
                    insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    camera_id INT NOT NULL REFERENCES camera(id),
                    event_type varchar(256),
                    payload TEXT
                );
                """
            )
            cur.execute(
                """
                CREATE OR REPLACE FUNCTION camera_event_notify()
                    RETURNS trigger AS
                $$
                BEGIN
                    PERFORM pg_notify(
                        'camera_event_channel',
                        NEW.event_type::text || '|' || NEW.camera_id::text || '|' || NEW.payload::text
                    );
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                """
            )
            cur.execute(
                """
                CREATE TRIGGER camera_event_update AFTER INSERT
                    ON camera_event
                    FOR EACH ROW
                EXECUTE PROCEDURE camera_event_notify();
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
