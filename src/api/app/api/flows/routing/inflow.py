from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from api.db.session import get_session

from api.flows.models.inflow import (
    InflowCreateSchema,
    InflowModel,
    InflowListSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

# POST /api/inflow/
@router.post("/", response_model=InflowModel)
def send_inflow(payload: InflowCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = InflowModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# GET /api/inflow/{user_id}
@router.get("/{user_id}", response_model=InflowListSchema)
def send_outflow(user_id: int, session: Session = Depends(get_session)):
    query = select(InflowModel).where(InflowModel.userId == user_id).order_by(InflowModel.inflowId)
    results = session.exec(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="Inflow not found") 
    return {"results": results, "count": len(results)}

# GET /api/inflow/{inflow_id}
@router.get("/{inflow_id}", response_model=InflowModel)
def get_inflow_by_id(inflow_id: int, session: Session = Depends(get_session)):
    query = select(InflowModel).where(InflowModel.inflowId == inflow_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Inflow not found")
    return result