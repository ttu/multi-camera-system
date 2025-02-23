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

#### PoC Communication

![System](docs/poc_communication.excalidraw.png)

#### Detection with BLE Sensors & Recording

![Detection](docs/detection.excalidraw.png)

### Run with Docker Compose

```sh
cd multi-camera-system
chmod +x setup.sh
./setup.sh
```

Open `http://localhost:8000/site` to see the Server Side UI.

Open `http://localhost:5173` to see the Client Side UI.

#### Run Only External Containers For Development

```sh
./setup.sh
docker compose down && docker compose up -d postgres minio
```

Camera's inside Docker do not work at the moment. That is due how Docker handles the network. If `host.docker.internal` is used as `SERVER_HOST` in `.env`, camera's will have own ip address (`172.20.0.x`), but the server will see those as from different hosts (`127.0.0.1`).

#### Start Containers for Debugging

`docker-compose.yml` has a command for starting container with `debugpy`. It will wait for client to connect before starting the server. Check VS Code Docker debug start command from `launch.json`.

### Install Development Environment

Requirements

```sh
asdf install
```

Server

```sh
cd multi-camera-server

# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
# uv pip install -e .\[dev\]  # zsh

# Or using traditional pip
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
# python -m pip install -e .\[dev\]  # zsh

cp .env.example .env
```

Front-end

```sh
cd multi-camera-ui
npm install
npm run dev
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

Check `DB_CONNECTION` from `.env`.

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

Update access and secret key from `.env`.

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

### Docker

Create network to connect containers

```sh
docker network create camera-network
docker network connect camera-network postgres
docker network connect camera-network minio
```

Change connections strings in `.env` file

```py
# Use host name instead of IP address
SERVER_HOST="camera-server"
DB_CONNECTION="postgres://postgres:mysecretpassword@postgres:5432/camera_db"
MINIO_ENDPOINT="minio:9000"
# Change host ip and base path
UVICORN_HOST="0.0.0.0"
UVICORN_BASE_PATH="/app/src/"
```

Start containers

```sh
docker build -t camera-system .
docker run --name camera-server --network camera-network -p 8000:8000 --rm camera-system python src/server_main.py
docker run --name camera-camera --network camera-network --rm camera-system python src/camera_main.py --dummy-mode True
```
