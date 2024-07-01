from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import *

router = APIRouter(prefix="/api/others", tags=["Others"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 抓到指定config底下所有audio id
@router.get("/{config_id}/audios", response_model=List[int])
def get_audio_ids_by_config(config_id: int, db: Session = Depends(get_database)):
    try:
        config = db.query(Config).filter(Config.id == config_id).first()
        if not config:
            raise HTTPException(status_code=404, detail="Config not found")
        audio_ids = [audio.audio_id for audio in config.audios]
        return audio_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# audio由指定type一次抓出所有那個類型的index
@router.get("/audios/type/{audio_type}", response_model=List[int])
def get_audio_ids_by_type(audio_type: str, db: Session = Depends(get_database)):
    try:
        audio_files = db.query(AudioFile).filter(AudioFile.type == audio_type).all()
        if not audio_files:
            raise HTTPException(status_code=404, detail="No audios found for the given type")
        audio_ids = [audio.id for audio in audio_files]
        return audio_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 用指定interaction_type去抓出那幾個config
@router.get("/interaction_type/{interaction_type}", response_model=List[int])
def get_configs_by_interaction_type(interaction_type: str, db: Session = Depends(get_database)):
    try:
        configs = db.query(Config).filter(Config.interaction_type == interaction_type).all()
        if not configs:
            raise HTTPException(status_code=404, detail="No configs found for the given interaction type")
        config_ids = [config.id for config in configs]
        return config_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 抓取指定track底下所有event
@router.get("/{track_id}/events", response_model=List[int])
def get_events_by_track(track_id: int, db: Session = Depends(get_database)):
    try:
        track = db.query(Track).filter(Track.id == track_id).first()
        if not track:
            raise HTTPException(status_code=404, detail="Track not found")
        event_ids = [event.id for event in track.events]
        return event_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 抓取指定event底下所有action
@router.get("/events/{event_id}/actions", response_model=List[int])
def get_actions_by_event(event_id: int, db: Session = Depends(get_database)):
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        action_ids = [action.id for action in event.actions]
        return action_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 抓取指定genre的所有audio
@router.get("/audios/genre/{genre}", response_model=List[int])
def get_audio_ids_by_genre(genre: str, db: Session = Depends(get_database)):
    try:
        audio_files = db.query(AudioFile).filter(AudioFile.genre == genre).all()
        if not audio_files:
            raise HTTPException(status_code=404, detail="No audios found for the given genre")
        audio_ids = [audio.id for audio in audio_files]
        return audio_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
