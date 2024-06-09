from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Fixed typo in 'CORSMiddleware'
from loguru import logger
import os
import time
import datetime
# Local Application Imports
from database import Base, engine
import endpoint as endpoint

# Create tables in the database (if they don't exist already)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sonicstride 音樂存取")

# Adding CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,  # Fixed typo in 'CORSMiddleware'
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials such as cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Setting the timezone to Asia/Taipei
os.environ["TZ"] = "Asia/Taipei"
time.tzset()

# Configuring logger to create a new log file daily at midnight, 
# with UTF-8 encoding, and retaining logs for 30 days
logger.add(
    "./logs/{time}.log",  # Log file path
    rotation=datetime.time(0, 0, 0),  # Rotate daily at midnight
    encoding="utf-8",  # File encoding
    retention="30 days",  # Keep logs for 30 days
    level="DEBUG",  # Log level
)

# Asynchronous function to log incoming requests
async def log_request(request: Request):
    logger.info(f"[{request.client.host}] {request.method} {request.url}")

# Including the router from the endpoint module and adding log_request as a dependency
app.include_router(endpoint.ROUTER, dependencies=[Depends(log_request)])

# Middleware to limit file upload size to 100MB
@app.middleware("http")
async def limit_upload_size(request, call_next):
    if request.url.path == "/api/music/upload" and request.method == "POST":
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > 100 * 1024 * 1024:  # 100MB limit
            return JSONResponse(content={"detail": "File too large"}, status_code=413)
    return await call_next(request)