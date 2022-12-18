import asyncio
import sys
from multiprocessing import Process

import uvicorn

import camera_main
import server_main

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    camera_1 = Process(target=camera_main.main_loop, args=[0, True], daemon=True)
    camera_1.start()
    camera_2 = Process(target=camera_main.main_loop, args=[1, True], daemon=True)
    camera_2.start()

    uvicorn.run(server_main.app, host="127.0.0.1", port=8000)
