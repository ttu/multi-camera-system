# Use the official Python base image with the desired version
FROM python:3.13.2-slim

RUN apt-get update
RUN apt install -y libopencv-dev python3-opencv

# Set the working directory in the container
WORKDIR /app

# Install debugpy and uv
RUN pip install debugpy uv

COPY pyproject.toml .
RUN uv pip install --system .

# Copy the application code to the container
COPY . .

# Set the entry point for the container
# CMD ["python", "camera_main.py", "--dummy-mode", "True"]
# CMD ["python", "server_main.py"]
# ENTRYPOINT [ "python" ]

# Expose the port for the FastAPI application and debugger
EXPOSE 8000 5678

# Command to run the application with debugger enabled
CMD ["python",  "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "src.server_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
