import sys

from dotenv import load_dotenv


load_dotenv()

import data_store
import event_handler

from common_types import EventType


if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else 0

    is_recording = data_store.get_camera_recording(id)
    event = EventType.CAMERA_COMMAND_STOP_RECORD if is_recording else EventType.CAMERA_COMMAND_RECORD
    result = event_handler.send_event(event, id)

    print("New state", {"camera_id": id, "event": event.value})
