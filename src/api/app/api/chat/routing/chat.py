# api/chat/routing/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from api.db.session import get_session

from api.chat.models.chat import (
    ChatModel,
    ChatCreateSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

# POST /api/Chat/
@router.post("/", response_model=ChatModel)
def send_Chat(payload: ChatCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = ChatModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# GET /api/chat/{user_id}
@router.get("/{user_id}", response_model=ChatModel)
def get_chat(user_id: int, session: Session = Depends(get_session)):
    query = select(ChatModel).where(ChatModel.userId == user_id)
    result = session.exec(query).first() 
    if not result:
        raise HTTPException(status_code=404, detail="Chat not found")
    return result 



