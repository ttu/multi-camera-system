from typing import AsyncGenerator, Generator, Tuple

import psycopg

import common_config
from common_types import EventType

# pylint: disable=not-context-manager


def wait_for_events(
    event_types: list[EventType], identifier: int | None = None
) -> Generator[Tuple[str, Tuple[str, str]], None, None]:
    events_to_listen = [event.value for event in event_types]
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        conn.execute("LISTEN camera_event_channel;")
        conn.commit()
        gen = conn.notifies()
        for event in gen:
            # payload: {event_type}|{camera_id}|{payload}
            payload = event.payload.split("|")
            if payload[0] in events_to_listen:
                if identifier is None:
                    yield payload[0], (payload[1], payload[2])
                if payload[1] == str(identifier):
                    yield payload[0], (payload[1], payload[2])


async def wait_for_events_async(
    event_types: list[EventType], identifier: int | None = None
) -> AsyncGenerator[Tuple[str, Tuple[str, str]], None]:
    events_to_listen = [event.value for event in event_types]
    async with await psycopg.AsyncConnection.connect(common_config.DB_CONNECTION) as conn:
        await conn.execute("LISTEN camera_event_channel;")
        await conn.commit()
        async for event in conn.notifies():
            # payload: {event_type}|{camera_id}|{payload}
            payload = event.payload.split("|")
            if payload[0] in events_to_listen:
                if not identifier:
                    yield payload[0], (payload[1], payload[2])
                if payload[1] == str(identifier):
                    yield payload[0], (payload[1], payload[2])


def send_event(event_type: EventType, camera_id: int, payload: str = "") -> bool:
    with psycopg.connect(common_config.DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            # cur.execute(f"NOTIFY camera_event_channel, '{event_type.value}:{camera_id}:{payload}';")
            cur.execute(
                "INSERT INTO camera_event (camera_id, event_type, payload) VALUES (%s, %s, %s)",
                (camera_id, event_type.value, payload),
            )
            return cur.rowcount > 0
