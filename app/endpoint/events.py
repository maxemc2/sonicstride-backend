from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models import Event, Track

router = APIRouter(prefix="/api/events", tags=["Events"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for Event
class EventCreate(BaseModel):
    track_id: int
    type: str

class EventUpdate(BaseModel):
    track_id: Optional[int] = None
    type: Optional[str] = None

# Endpoint to list all events
@router.get("/list", response_model=List[dict])
def list_events(db: Session = Depends(get_database)):
    events_list = db.query(Event).all()
    return [{"id": event.id, "track_id": event.track_id, "type": event.type} for event in events_list]

# Endpoint to create a new event
@router.post("/", response_model=dict)
def create_event(event: EventCreate, db: Session = Depends(get_database)):
    # Check if the Track id exists in the database
    config = db.query(Track).filter(Track.id == event.track_id).first()
    if not config:
        raise HTTPException(status_code=404, detail=f"Track ID {event.track_id} not found")
    
    db_event = Event(
        track_id=event.track_id,
        type=event.type
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return {"id": db_event.id, "track_id": db_event.track_id, "type": db_event.type}

# Endpoint to delete an event
@router.delete("/{event_id}", response_model=dict)
def delete_event(event_id: int, db: Session = Depends(get_database)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}

# Endpoint to update an event
@router.put("/{event_id}", response_model=dict)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_database)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return {"id": db_event.id, "track_id": db_event.track_id, "type": db_event.type}

# Endpoint to delete all events
@router.delete("/delete_all", response_model=dict)
def delete_all_events(db: Session = Depends(get_database)):
    db.query(Event).delete()
    db.commit()
    return {"message": "All events deleted successfully"}