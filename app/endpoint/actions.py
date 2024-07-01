from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models import Action, Event

router = APIRouter(prefix="/api/actions", tags=["Actions"])

# Dependency to get a database session
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for Action
class ActionCreate(BaseModel):
    event_id: int
    target: str
    property: str
    method: str
    value: float
    end_time: float

class ActionUpdate(BaseModel):
    target: Optional[str] = None
    property: Optional[str] = None
    method: Optional[str] = None
    value: Optional[float] = None
    end_time: Optional[float] = None

# Endpoint to list all actions
@router.get("/list", response_model=List[dict])
def list_actions(db: Session = Depends(get_database)):
    actions_list = db.query(Action).all()
    return [{"id": action.id, "event_id": action.event_id, "target": action.target, "property": action.property, "method": action.method, "value": action.value, "end_time": action.end_time} for action in actions_list]

# Endpoint to create a new action
@router.post("/", response_model=dict)
def create_action(action: ActionCreate, db: Session = Depends(get_database)):
    # Check if the Event id exists in the database
    config = db.query(Event).filter(Event.id == action.event_id).first()
    if not config:
        raise HTTPException(status_code=404, detail=f"Event ID {action.event_id} not found")
    
    db_action = Action(
        event_id=action.event_id,
        target=action.target,
        property=action.property,
        method=action.method,
        value=action.value,
        end_time=action.end_time
    )
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return {"id": db_action.id, "event_id": db_action.event_id, "target": db_action.target, "property": db_action.property, "method": db_action.method, "value": db_action.value, "end_time": db_action.end_time}

# Endpoint to delete an action
@router.delete("/{action_id}", response_model=dict)
def delete_action(action_id: int, db: Session = Depends(get_database)):
    db_action = db.query(Action).filter(Action.id == action_id).first()
    if not db_action:
        raise HTTPException(status_code=404, detail="Action not found")
    db.delete(db_action)
    db.commit()
    return {"message": "Action deleted successfully"}

# Endpoint to update an action
@router.put("/{action_id}", response_model=dict)
def update_action(action_id: int, action: ActionUpdate, db: Session = Depends(get_database)):
    db_action = db.query(Action).filter(Action.id == action_id).first()
    if not db_action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    update_data = action.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_action, key, value)
    
    db.commit()
    db.refresh(db_action)
    return {"id": db_action.id, "event_id": db_action.event_id, "target": db_action.target, "property": db_action.property, "method": db_action.method, "value": db_action.value, "end_time": db_action.end_time}

# Endpoint to delete all actions
@router.delete("/delete_all", response_model=dict)
def delete_all_actions(db: Session = Depends(get_database)):
    db.query(Action).delete()
    db.commit()
    return {"message": "All actions deleted successfully"}