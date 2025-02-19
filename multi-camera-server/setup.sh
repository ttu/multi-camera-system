echo "Stopping existing containers..."
docker compose down

docker compose up -d minio

echo "Starting Postgres..."
docker compose up -d --wait postgres

echo "Creating database..."
docker exec -it postgres psql "postgres://postgres:mysecretpassword@localhost:5432/postgres" -c "DROP DATABASE IF EXISTS camera_db"
docker exec -it postgres psql "postgres://postgres:mysecretpassword@localhost:5432/postgres" -c "CREATE DATABASE camera_db"

echo "Seeding database..."
docker compose run --rm camera-server bash -c "python src/db_create_initial_data.py"

echo "Configuring MinIO..."

echo "Waiting for MinIO to be fully initialized..."
docker compose up -d --wait minio

echo "Reading MinIO credentials from .env.example..."
echo "Reading MinIO credentials from .env.example..."
ACCESS_KEY=$(grep MINIO_ACCESS_KEY .env.example | cut -d'"' -f2)
SECRET_KEY=$(grep MINIO_SECRET_KEY .env.example | cut -d'"' -f2)

echo "Configuring MinIO admin access..."
docker exec -it minio mc alias set local http://localhost:9000 root mysecretpassword

echo "Creating MinIO access keys..."
docker exec -it minio mc admin accesskey create local/ root \
    --access-key "${ACCESS_KEY}" \
    --secret-key "${SECRET_KEY}"

echo "Creating and configuring bucket..."
docker exec -it minio mc mb local/camera-system-bucket

echo "Setting bucket permissions..."
docker exec -it minio mc anonymous set download local/camera-system-bucket

echo "MinIO configuration completed with:"
echo "Access Key: ${ACCESS_KEY}"
echo "Secret Key: ${SECRET_KEY}"

echo "Starting remaining services..."
docker compose up -d 