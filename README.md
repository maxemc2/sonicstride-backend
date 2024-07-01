Here's the updated README with the additional notes:

---

# Sonicstride Backend of MusicStream

<p align="left">
  <a href="https://fastapi.tiangolo.com/" alt="fastapi"><img src="https://img.shields.io/badge/fastapi-v0.78.0-blue" /></a>
  <a href="https://www.docker.com/" alt="docker"><img src="https://img.shields.io/badge/docker-v20.10.7-blue" /></a>
</p>

### Project Description
MusicStream is a FastAPI application that allows users to select music from a dropdown menu and play it on a webpage using the Web Audio API. Users can also upload their own music files in MP3 or WAV format to the database.

## Application Features
- **Music Playback**: Users can select and play music from a predefined list.
- **Music Upload**: Users can upload MP3 or WAV music files to the database.
- **Web Audio API**: Utilizes the Web Audio API for playing music directly on the webpage.

### External API Endpoints
- **GET /api/music/**: Returns a list of available music tracks.
- **GET /api/music/{id}/**: Returns details of a specific music track by ID.
- **POST /api/music/upload/**: Allows users to upload a music file.

## Installation and Configuration

1. Download the project:
    ```bash
    git clone https://github.com/maxemc2/sonicstride-backend
    cd sonicstride-backend
    ```

2. Configure the settings in `docker-compose.yml` as needed.

3. Generate a self-signed certificate and private key:
    ```bash
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/www_sonicstride_app.key -out /etc/ssl/certs/www_sonicstride_app.crt
    ```

4. Install Docker and Docker Compose:
    - Docker: [Official Installation Documentation](https://docs.docker.com/get-docker/)
    - Docker Compose: [Official Installation Documentation](https://docs.docker.com/compose/install/)

5. Use `docker-compose` commands to run and stop the application:
    - To run:
    ```bash
    docker-compose up
    ```
    - To stop:
    ```bash
    docker-compose down
    ```

## Package List
- fastapi==0.78.0
- uvicorn==0.17.6
- pipenv==2023.5.20

### Overview
- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for serving FastAPI applications.
- **Docker**: Used for containerizing the application.
- **Pipenv**: Used for managing Python dependencies.

### Notes

#### Transmission Rate and File Handling
- **Supported File Size**: Up to 100MB.
- **Transmission Rate**: Recommended minimum bandwidth is 20 Mbps to support efficient file upload and download.
- **File Formats**: Supports MP3 and WAV formats.

#### Security
- Use HTTPS to secure all API communications.
- (To be completed) Scan uploaded music files to prevent malware propagation.