import asyncio

from bleak import BleakScanner

from sensor_toggle_record import set_recording

MACS_TO_LISTEN = ["61:13:C3:CE:7D:4D", "CD:D4:FA:52:7A:F2"]
TARGET_RECORD_STRENGTH = -50
TARGET_STOP_STRENGTH = -70
CAMERA_ID = 0


async def main():
    while True:
        devices = await BleakScanner.discover(timeout=1)
        for device in devices:
            # if d.rssi > -40:
            if device.address in MACS_TO_LISTEN and device.rssi > TARGET_RECORD_STRENGTH:
                print("Found", {"address": device.address, "name": device.name, "rssi": device.rssi})
                set_recording(CAMERA_ID, True)
            if device.address in MACS_TO_LISTEN and device.rssi < TARGET_STOP_STRENGTH:
                print("Found", {"address": device.address, "name": device.name, "rssi": device.rssi})
                set_recording(CAMERA_ID, False)


if __name__ == "__main__":
    asyncio.run(main())
