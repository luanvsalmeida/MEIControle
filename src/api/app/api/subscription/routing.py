from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from api.db.session import get_session

from api.subscription.models import (
    SubscriptionModel,
    SubscriptionCreateSchema,
    SubscriptionListSchema,
    SubscriptionUpdateSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

# POST /api/subscription/
@router.post("/", response_model=SubscriptionModel)
def send_Subscription(payload: SubscriptionCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = SubscriptionModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# GET /api/subscription/{subscription_id}
@router.get("/by_user/{subscription_id}", response_model=SubscriptionListSchema)
def get_Subscription(subscription_id: int, session: Session = Depends(get_session)): 
    query = select(SubscriptionModel).where(SubscriptionModel.subscriptionId == subscription_id).order_by(SubscriptionModel.subscriptionId)
    results = session.exec(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return {"results": results, "count": len(results)}


# GET /api/subscription/{subscription_id}
@router.get("/by_subscription/{subscription_id}", response_model=SubscriptionModel)
def get_Subscription(subscription_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(SubscriptionModel).where(SubscriptionModel.subscriptionId == subscription_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return result

# PUT /api/subscription/{subscription_id}
@router.put("/{subscription_id}", response_model=SubscriptionModel)
def edit_account(subscription_id: int,
                 payload: SubscriptionUpdateSchema,
                 session: Session = Depends(get_session)):
    query = select(SubscriptionModel).where(SubscriptionModel.subscriptionId == subscription_id)
    obj = session.exec(query).first()
    if not obj: 
        raise HTTPException(status_code=404, detail="Subscription not found")

    data = payload.model_dump()

    for k, v in data.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj