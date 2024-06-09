from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from pydantic import UUID4
from typing import Optional, List
from sqlalchemy.orm import Session
import os, re
from loguru import logger
# Local Application Imports
from database import SessionLocal
from model import *

router = APIRouter(prefix="/api/music", tags=["Request to musics"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to list all music
@router.get("/list", response_model=List[dict])
def list_music(db: Session = Depends(get_database)):
    music_list = db.query(MusicsModel).all()
    return [{"id": str(music.id), "song_name": music.song_name, "file_path": music.music_file} for music in music_list]

# Endpoint to download music by ID
@router.get("/download/{id}")
def download_music(id: UUID4, db: Session = Depends(get_database)):
    music = db.query(MusicsModel).filter(MusicsModel.id == id).first()
    if music is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return FileResponse(path=music.music_file, filename=os.path.basename(music.music_file))

# Function to validate track_id format
def validate_track_id(track_id: str):
    pattern = r'^\d{2}[A-Z]-\d{3}-V\d$'
    if not re.match(pattern, track_id):
        raise HTTPException(status_code=400, detail="Invalid track ID format. Expected format: '01A-001-V1'")

# Endpoint to upload music
@router.post("/upload")
async def upload_music(
    experiment_title: str = Form(..., description="Title of the experiment"),
    default_scene: SceneEnum = Form(..., description="Default scene for playback (e.g., Running, Walking)"),
    genre: GenreEnum = Form(..., description="Music genre (e.g., Ambient, Nature Sounds)"),
    bpm: Optional[int] = Form(None, description="Beats Per Minute, optional"),
    key: Optional[str] = Form(None, description="Musical key, optional"),
    song_name: str = Form(..., description="Name of the song"),
    track_id: str = Form(..., description="Track ID in the format '01A-001-V1'"),
    music_file: UploadFile = File(..., description="Music file (MP3, WAV)"),
    db: Session = Depends(get_database)
):
    validate_track_id(track_id)  # Validate track_id format

    # Ensure the 'files/' directory exists
    os.makedirs("files", exist_ok=True)
    file_location = os.path.join("files", music_file.filename)
    logger.info(f"Saving file to {file_location}")

    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(music_file.file.read())
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error while saving file")

    db_music = MusicsModel(
        experiment_title=experiment_title,
        default_scene=default_scene,
        genre=genre,
        bpm=bpm,
        key=key,
        song_name=song_name,
        track_id=track_id,
        music_file=file_location
    )
    
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    db.close()
    
    return {"success": True, "message": "File uploaded successfully"}