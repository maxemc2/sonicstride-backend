from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models import Config, AudioFile, ConfigAudio

router = APIRouter(prefix="/api/configs", tags=["Configs"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for Config
class ConfigCreate(BaseModel):
    name: str
    author: Optional[str] = "Sonicstride"
    interaction_type: Optional[str] = None
    bpm: Optional[int] = None
    labels: Optional[str] = None
    audio_ids: List[int] = Field(default=[])

class ConfigUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    interaction_type: Optional[str] = None
    bpm: Optional[int] = None
    labels: Optional[str] = None
    audio_ids: Optional[List[int]] = None

# Endpoint to list all configs
@router.get("/list", response_model=List[dict])
def list_configs(db: Session = Depends(get_database)):
    configs_list = db.query(Config).all()
    return [
        {
            "id": config.id,
            "name": config.name,
            "author": config.author,
            "interaction_type": config.interaction_type,
            "bpm": config.bpm,
            "create_time": config.create_time,
            "labels": config.labels,
            "audios": [{"id": audio.audio_file.id, "name": audio.audio_file.name} for audio in config.audios]
        } for config in configs_list
    ]

# Endpoint to create a new config
@router.post("/", response_model=dict)
def create_config(config: ConfigCreate, db: Session = Depends(get_database)):
    db_config = Config(
        name=config.name,
        author=config.author,
        interaction_type=config.interaction_type,
        bpm=config.bpm,
        labels=config.labels
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)

    # Add the audio files associations
    for audio_id in config.audio_ids:
        audio_file = db.query(AudioFile).filter(AudioFile.id == audio_id).first()
        if not audio_file:
            raise HTTPException(status_code=404, detail=f"AudioFile ID {audio_id} not found")
        config_audio = ConfigAudio(config_id=db_config.id, audio_id=audio_id)
        db.add(config_audio)

    db.commit()
    db.refresh(db_config)

    return {
        "id": db_config.id,
        "name": db_config.name,
        "author": db_config.author,
        "interaction_type": db_config.interaction_type,
        "bpm": db_config.bpm,
        "create_time": db_config.create_time,
        "labels": db_config.labels,
        "audios": [{"id": audio.audio_file.id, "name": audio.audio_file.name} for audio in db_config.audios]
    }

# Endpoint to delete a config
@router.delete("/{config_id}", response_model=dict)
def delete_config(config_id: int, db: Session = Depends(get_database)):
    db_config = db.query(Config).filter(Config.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Config not found")
    db.query(ConfigAudio).filter(ConfigAudio.config_id == config_id).delete()
    db.delete(db_config)
    db.commit()
    return {"message": "Config deleted successfully"}

# Endpoint to update a config
@router.put("/{config_id}", response_model=dict)
def update_config(config_id: int, config: ConfigUpdate, db: Session = Depends(get_database)):
    db_config = db.query(Config).filter(Config.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Config not found")
    
    update_data = config.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_config, key, value)
    
    db.commit()

    # Update the audio files associations
    if config.audio_ids is not None:
        db.query(ConfigAudio).filter(ConfigAudio.config_id == config_id).delete()
        for audio_id in config.audio_ids:
            audio_file = db.query(AudioFile).filter(AudioFile.id == audio_id).first()
            if not audio_file:
                raise HTTPException(status_code=404, detail=f"AudioFile ID {audio_id} not found")
            config_audio = ConfigAudio(config_id=db_config.id, audio_id=audio_id)
            db.add(config_audio)

    db.commit()
    db.refresh(db_config)

    return {
        "id": db_config.id,
        "name": db_config.name,
        "author": db_config.author,
        "interaction_type": db_config.interaction_type,
        "bpm": db_config.bpm,
        "create_time": db_config.create_time,
        "labels": db_config.labels,
        "audios": [{"id": audio.audio_file.id, "name": audio.audio_file.name} for audio in db_config.audios]
    }

# Endpoint to delete all configs
@router.delete("/delete_all", response_model=dict)
def delete_all_configs(db: Session = Depends(get_database)):
    db.query(Config).delete()
    db.commit()
    return {"message": "All configs deleted successfully"}