from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from loguru import logger
from database import SessionLocal
from models import AudioFile, GenreEnum

router = APIRouter(prefix="/api/audiofiles", tags=["AudioFiles"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for AudioFile update
class AudioFileUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    type: Optional[str] = None
    genre: Optional[GenreEnum] = None
    key: Optional[str] = None
    bpm: Optional[int] = None

# Endpoint to list all audio files with important information
@router.get("/list", response_model=List[dict])
def list_audio_files(db: Session = Depends(get_database)):
    audio_files_list = db.query(AudioFile).all()
    return [
        {
            "id": audio_file.id,
            "name": audio_file.name,
            "author": audio_file.author,
            "genre": audio_file.genre,
            "file_path": audio_file.file_path
        } for audio_file in audio_files_list
    ]

# Endpoint to create a new audio file with file upload
@router.post("/", response_model=dict)
async def create_audio_file(
    name: str = Form(..., description="Name of the audio file"),
    author: Optional[str] = Form(None, description="Author of the audio file"),
    type: str = Form(..., description="Type of the audio file (e.g., section, sample)"),
    genre: Optional[GenreEnum] = Form(None, description="Music genre"),
    key: Optional[str] = Form(None, description="Musical key, optional"),
    bpm: Optional[int] = Form(None, description="Beats Per Minute, optional"),
    audio_file: UploadFile = File(..., description="Audio file (MP3, WAV)"),
    db: Session = Depends(get_database)
):
    os.makedirs("audio_files", exist_ok=True)
    file_location = os.path.join("audio_files", audio_file.filename)
    logger.info(f"Saving file to {file_location}")

    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(audio_file.file.read())
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error while saving file")

    db_audio_file = AudioFile(
        name=name,
        author=author,
        type=type,
        genre=genre,
        key=key,
        bpm=bpm,
        file_path=file_location
    )
    
    db.add(db_audio_file)
    db.commit()
    db.refresh(db_audio_file)
    return {
        "name": db_audio_file.name,
        "author": db_audio_file.author,
        "type": db_audio_file.type,
        "genre": db_audio_file.genre,
        "key": db_audio_file.key,
        "bpm": db_audio_file.bpm,
        "file_path": db_audio_file.file_path
    }

# Endpoint to delete an audio file
@router.delete("/{audio_file_id}", response_model=dict)
def delete_audio_file(audio_file_id: str, db: Session = Depends(get_database)):
    db_audio_file = db.query(AudioFile).filter(AudioFile.id == audio_file_id).first()
    if not db_audio_file:
        raise HTTPException(status_code=404, detail="AudioFile not found")
    db.delete(db_audio_file)
    db.commit()
    return {"message": "AudioFile deleted successfully"}

# Endpoint to update an audio file
@router.put("/{audio_file_id}", response_model=dict)
def update_audio_file(audio_file_id: str, audio_file: AudioFileUpdate, db: Session = Depends(get_database)):
    db_audio_file = db.query(AudioFile).filter(AudioFile.id == audio_file_id).first()
    if not db_audio_file:
        raise HTTPException(status_code=404, detail="AudioFile not found")
    
    update_data = audio_file.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_audio_file, key, value)
    
    db.commit()
    db.refresh(db_audio_file)
    return {
        "id": db_audio_file.id,
        "name": db_audio_file.name,
        "author": db_audio_file.author,
        "type": db_audio_file.type,
        "genre": db_audio_file.genre,
        "key": db_audio_file.key,
        "bpm": db_audio_file.bpm,
        "file_path": db_audio_file.file_path
    }

# Endpoint to download audio file by ID
@router.get("/download/{id}")
def download_audio_file(id: str, db: Session = Depends(get_database)):
    audio_file = db.query(AudioFile).filter(AudioFile.id == id).first()
    if audio_file is None:
        raise HTTPException(status_code=404, detail="AudioFile not found")
    return FileResponse(path=audio_file.file_path, filename=os.path.basename(audio_file.file_path))


# Endpoint to delete all audio files
@router.delete("/delete_all", response_model=dict)
def delete_all_audio_files(db: Session = Depends(get_database)):
    db.query(AudioFile).delete()
    db.commit()
    return {"message": "All audio files deleted successfully"}