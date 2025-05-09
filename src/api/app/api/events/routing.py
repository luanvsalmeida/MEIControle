import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.db.session import get_session

from .models import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)
router  = APIRouter()
from api.db.config import DATABASE_URL
# GET/api/events/
@router.get("/", response_model=EventListSchema)
def read_event(session: Session = Depends(get_session)) -> EventListSchema:
    print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    query = select(EventModel).order_by(EventModel.id.desc()).limit(5)
    results = session.exec(query).all()
    return {
        "results": results,
        "count": len(results)
    }


# POST/api/events/
@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema, 
    session: Session = Depends(get_session)):
    print(type(payload.page)) 
    data = payload.model_dump() # payload -> dict -> pydantic
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj 


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id:int, 
                 payload: EventUpdateSchema,
                 session: Session = Depends(get_session)): 
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    
    data = payload.model_dump() # payload -> dict -> pydantic
    
    for k, v in data.items():   # for key value
        setattr(obj, k, v)      # set attribute for obj 

    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj