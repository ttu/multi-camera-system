# multi-camera-system

System for controlling multiple cameras

### Install

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install .[dev]
```

### Run

```sh
# create database
python src/db_create_initial_data.py
# start server
python src/server_main.py
# start camera
python src/camera_main.py
```

Start the camera in dummy mode
```sh
python src/camera_main.py --dummy-mode True
```
### Process

#### System
![System](docs/system.excalidraw.png)

#### PoC communication
![System](docs/poc_communication.excalidraw.png)

#### Detection with BLE sensors & recording
![Detection](docs/detection.excalidraw.png)


```
User selects activate from web UI
  Send start with BLE Id to server

Server receives start request
  Get configuration
  Send ready signal with BLE Id to all configured cameras

Camera computer receives ready signal with BLE device Id
  Start camera
  Start detecting BLE signal for device Id

  Receive BLE signal
    Start recording

  Loose BLE signal
    Stop recording
    Stop camera
```
