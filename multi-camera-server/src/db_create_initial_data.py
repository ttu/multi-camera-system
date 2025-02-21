import psycopg

from dotenv import load_dotenv


load_dotenv()

import common_config


# pylint: disable=not-context-manager


def create_db():
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE route (
                    id INTEGER NOT NULL PRIMARY KEY,
                    name TEXT
                );
                """
            )
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
                CREATE TABLE route_cameras (
                    route_id INTEGER NOT NULL REFERENCES route(id),
                    camera_id INTEGER NOT NULL REFERENCES camera(id)
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE camera_event (
                    id SERIAL PRIMARY KEY,
                    insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    camera_id INTEGER NOT NULL REFERENCES camera(id),
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
    route_sql = "INSERT INTO route (id, name) values(%s, %s)"
    route_data = [(0, "A-Line"), (1, "Enduro Z"), (2, "World Cup")]
    camera_sql = "INSERT INTO camera (id, name) values(%s, %s)"
    camera_data = [
        (0, "A-Line start"),
        (1, "A-Line tabletop middle"),
        (2, "A-Line end forest drop"),
        (3, "Enduro Z South"),
        (4, "Enduro Z North"),
        (5, "World Cup road gap"),
    ]
    route_camera_sql = "INSERT INTO route_cameras (route_id, camera_id) values(%s, %s)"
    route_camera_data = [(0, 0), (0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]

    data_inputs = [(route_sql, route_data), (camera_sql, camera_data), (route_camera_sql, route_camera_data)]

    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            for sql, data in data_inputs:
                cur.executemany(sql, data)
                if cur.rowcount == 0:
                    print("Error")


create_db()
seed_db()
