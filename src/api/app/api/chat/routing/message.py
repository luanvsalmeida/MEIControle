import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from api.db.session import get_session

from api.chat.models.message import (
    MessageModel,
    MessageCreateSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

# POST /api/message/
@router.post("/", response_model=MessageModel)
def send_message(payload: MessageCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = MessageModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)

# GET /api/message/{chat_id}
@router.get("/{chat_id}", response_model=MessageModel)
def get_Message(chat_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(MessageModel).where(MessageModel.chatID == chat_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Message not found")
    return result

# GET /api/message/{message_id}
@router.get("/{message_id}", response_model=MessageModel)
def get_Message(message_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(MessageModel).where(MessageModel.messageId == message_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Message not found")
    return result