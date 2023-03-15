# multi-camera-system

System for controlling multiple cameras

### Tech stack

- React
- Fast API
- Python socket
- PostgreSQL
- Bleak BLE
- Vue3
- WebSocket

#### System

![System](docs/system.excalidraw.png)

#### PoC communication

![System](docs/poc_communication.excalidraw.png)

#### Detection with BLE sensors & recording

![Detection](docs/detection.excalidraw.png)

### Install

Server
```sh
cd multi-camera-server
python -m venv .venv
source .venv/bin/activate
python -m pip install .[dev]
```

Front-end
```sh
cd multi-camera-ui
npm install
```

#### Postgres

```sh
docker volume create postgres
docker run -d \
   -p 127.0.0.1:5432:5432 \
   -v postgres:/var/lib/postgresql/data \
   --name postgres \
   -e POSTGRES_PASSWORD=mysecretpassword \
   --restart always \
   postgres:14.4
```

```sh
docker exec -it postgres psql "postgres://postgres:mysecretpassword@localhost:5432/postgres" -c "DROP DATABASE camera_db"
docker exec -it postgres psql "postgres://postgres:mysecretpassword@localhost:5432/postgres" -c "CREATE DATABASE camera_db"
```

Check `DB_CONNECTION` from `common_config.py`.

NOTE: `psycopg` is installed in binary mode.

### MinIO

```sh
docker volume create minio
docker run \
   -p 9000:9000 \
   -p 9090:9090 \
   --name minio \
   -v minio:/data \
   -e "MINIO_ROOT_USER=root" \
   -e "MINIO_ROOT_PASSWORD=mysecretpassword" \
   --restart always \
   quay.io/minio/minio server /data --console-address ":9090"
```

Create a new access key from `http://127.0.0.1:9090/access-keys`.

Update access and secret key from `common_config.py`.

### Run

```sh
# create database
python src/db_create_initial_data.py
# start server
python src/server_main.py
# start camera
python src/camera_main.py
```

Open server site: `http://127.0.0.1:8000/site`

Start the camera in dummy mode

```sh
python src/camera_main.py --dummy-mode True
```
