# Base image
FROM python:3.12-slim

ARG ENVIRONMENT

EXPOSE 8080


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV YAML_CONFIG_FILE="/app/config/app-config.yaml"

# Set the working directory
WORKDIR /app

# Copy the requirements
COPY ./requirements.txt ./requirements.txt


# Build the dependencies
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


# Copy the code
COPY ./build/demo-sidecar/src/main.py ./main.py

COPY ./build/demo-sidecar/src/f7t-api-config.demo-env.yaml  ./config/app-config.yaml

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
