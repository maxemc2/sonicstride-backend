from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models import Config, Track

router = APIRouter(prefix="/api/tracks", tags=["Tracks"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for Track
class TrackCreate(BaseModel):
    config_id: str
    name: str
    type: str
    loop: Optional[bool] = None
    decay: Optional[bool] = None
    initial_gain: Optional[float] = None
    track_initial_gain: Optional[float] = None
    track_gain_node: Optional[dict] = None
    effect_nodes: Optional[dict] = None

class TrackUpdate(BaseModel):
    config_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    loop: Optional[bool] = None
    decay: Optional[bool] = None
    initial_gain: Optional[float] = None
    track_initial_gain: Optional[float] = None
    track_gain_node: Optional[dict] = None
    effect_nodes: Optional[dict] = None

# Endpoint to list all tracks
@router.get("/list", response_model=List[dict])
def list_tracks(db: Session = Depends(get_database)):
    tracks_list = db.query(Track).all()
    return [
        {
            "id": track.id,
            "config_id": track.config_id,
            "name": track.name,
            "type": track.type,
            "loop": track.loop,
            "decay": track.decay,
            "initial_gain": track.initial_gain,
            "track_initial_gain": track.track_initial_gain,
            "track_gain_node": track.track_gain_node,
            "effect_nodes": track.effect_nodes
        } for track in tracks_list
    ]

# Endpoint to create a new track
@router.post("/", response_model=dict)
def create_track(track: TrackCreate, db: Session = Depends(get_database)):
    # Check if the config_id exists in the database
    config = db.query(Config).filter(Config.id == track.config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail=f"Config ID {track.config_id} not found")
    
    db_track = Track(
        config_id=track.config_id,
        name=track.name,
        type=track.type,
        loop=track.loop,
        decay=track.decay,
        initial_gain=track.initial_gain,
        track_initial_gain=track.track_initial_gain,
        track_gain_node=track.track_gain_node,
        effect_nodes=track.effect_nodes
    )
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return {
        "id": db_track.id,
        "config_id": db_track.config_id,
        "name": db_track.name,
        "type": db_track.type,
        "loop": db_track.loop,
        "decay": db_track.decay,
        "initial_gain": db_track.initial_gain,
        "track_initial_gain": db_track.track_initial_gain,
        "track_gain_node": db_track.track_gain_node,
        "effect_nodes": db_track.effect_nodes
    }

# Endpoint to delete a track
@router.delete("/{track_id}", response_model=dict)
def delete_track(track_id: int, db: Session = Depends(get_database)):
    db_track = db.query(Track).filter(Track.id == track_id).first()
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    db.delete(db_track)
    db.commit()
    return {"message": "Track deleted successfully"}

# Endpoint to update a track
@router.put("/{track_id}", response_model=dict)
def update_track(track_id: int, track: TrackUpdate, db: Session = Depends(get_database)):
    db_track = db.query(Track).filter(Track.id == track_id).first()
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    update_data = track.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_track, key, value)
    
    db.commit()
    db.refresh(db_track)
    return {
        "id": db_track.id,
        "config_id": db_track.config_id,
        "name": db_track.name,
        "type": db_track.type,
        "loop": db_track.loop,
        "decay": db_track.decay,
        "initial_gain": db_track.initial_gain,
        "track_initial_gain": db_track.track_initial_gain,
        "track_gain_node": db_track.track_gain_node,
        "effect_nodes": db_track.effect_nodes
    }

# Endpoint to delete all tracks
@router.delete("/delete_all", response_model=dict)
def delete_all_tracks(db: Session = Depends(get_database)):
    db.query(Track).delete()
    db.commit()
    return {"message": "All tracks deleted successfully"}