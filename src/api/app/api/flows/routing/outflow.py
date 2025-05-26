# api/flows/routing/outflow.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.db.session import get_session

from api.flows.models.outflow import (
    OutflowCreateSchema,
    OutflowModel,
    OutflowListSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

# POST /api/Outflow/
@router.post("/", response_model=OutflowModel)
def send_outflow(payload: OutflowCreateSchema, session: Session = Depends(get_session)): 
    data = payload.model_dump()
    obj = OutflowModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# GET /api/Outflow/by_user/{user_id}
@router.get("/by_user/{user_id}", response_model=OutflowListSchema)
def get_outflow(user_id: int, session: Session = Depends(get_session)):
    query = select(OutflowModel).where(OutflowModel.userId == user_id).order_by(OutflowModel.outflowId)
    results = session.exec(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="Outflow not found") 
    return {"results": results, "count": len(results)}

# GET /api/Outflow/{outflow_id}
@router.get("/{outflow_id}", response_model=OutflowModel)
def get_outflow_by_id(outflow_id: int, session: Session = Depends(get_session)):
    query = select(OutflowModel).where(OutflowModel.outflowId == outflow_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Outflow not found")
    return result