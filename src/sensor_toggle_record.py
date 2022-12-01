import sys

from data_store import toggle_camera_recording

if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else 0
    recording_state = toggle_camera_recording(id)
    print("New state", {"camera_id": id, "recording": recording_state})
