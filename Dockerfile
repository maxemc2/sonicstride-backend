# FROM --platform=linux/amd64 python:3.9-slim
FROM python:3.9-slim

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip and pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock and install dependencies
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install

# Copy application code
COPY ./app /app

# Set working directory
WORKDIR /app

# Expose application port
EXPOSE 443

# Startup command
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]
# CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/etc/ssl/private/nginx-selfsigned.key", "--ssl-certfile", "/etc/ssl/certs/nginx-selfsigned.crt"]
