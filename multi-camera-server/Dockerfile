# Use the official Python base image with the desired version
FROM python:3.11.3-slim

RUN apt-get update
RUN apt install -y libopencv-dev python3-opencv

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY pyproject.toml .

# Install the Python dependencies
RUN python -m pip install .

# Copy the application code to the container
COPY . .

# Set the entry point for the container
# CMD ["python", "camera_main.py", "--dummy-mode", "True"]
# CMD ["python", "server_main.py"]
# ENTRYPOINT [ "python" ]