import sys

from data_store import toggle_camera_running

if __name__ == "__main__":
    args = sys.argv[1:]
    id = int(args[0]) if args else 0
    new_state = toggle_camera_running(id)
    print("New state", {"camera_id": id, "running": new_state})
