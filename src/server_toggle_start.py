import sys

from common_types import EventType
from data_store import get_camera_running
from event_handler import send_event

if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else 0

    is_running = get_camera_running(id)
    event = EventType.CAMERA_TURNOFF if is_running else EventType.CAMERA_PREPARE
    result = send_event(event, id)

    print("New state", {"camera_id": id, "event": event.value})
