from typing import Generator, Tuple

import psycopg

import common_config
from common_types import EventType

# pylint: disable=not-context-manager


def wait_for_events(event_types: list[EventType], identifier: int) -> Generator[Tuple[str, str], None, None]:
    events_to_listen = [event.value for event in event_types]
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        conn.execute("LISTEN camera_event_channel;")
        conn.commit()
        gen = conn.notifies()
        for event in gen:
            # payload: {event_type}:{camera_id}:{payload}
            payload = event.payload.split(":")
            if payload[0] in events_to_listen and payload[1] == str(identifier):
                yield payload[0], payload[1]


def send_event(event_type: EventType, camera_id: int, payload: str = "") -> bool:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            # cur.execute(f"NOTIFY camera_event_channel, '{event_type.value}:{camera_id}:{payload}';")
            cur.execute(
                "INSERT INTO camera_event (camera_id, event_type, payload) VALUES (%s, %s, %s)",
                (camera_id, event_type.value, payload),
            )
            return cur.rowcount > 0
