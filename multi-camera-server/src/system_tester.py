import asyncio
import sys
from multiprocessing import Process

import uvicorn

import camera_main
import common_config
import data_store
import server_main

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    routes = data_store.get_routes()
    # all_cameras = sum([r.cameras for r in routes], [])

    # For now start only route 1 cameras
    for camera in routes[0].cameras:
        camera_process = Process(target=camera_main.main_loop, args=[camera.camera_id, True], daemon=True)
        camera_process.start()

    # camera_process = Process(target=camera_main.main_loop, args=[0, False], daemon=True)
    # camera_process.start()

    uvicorn.run(server_main.app, host=common_config.UVICORN_HOST, port=common_config.UVICORN_PORT)
