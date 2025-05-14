from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from api.db.session import get_session
from api.services.nlp.interpreter import interpretar_mensagem

from api.chat.models.message import (
    MessageModel,
    MessageCreateSchema,
    MessageListSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

# POST /api/message/
@router.post("/", response_model=MessageModel)
def send_message(payload: MessageCreateSchema, session: Session = Depends(get_session)):
    # text interpretation
    texto = payload.content
    resultado = interpretar_mensagem(texto)  # <- aqui você chama o helper
    print(resultado)
    # store the message in the database
    data = payload.model_dump()
    obj = MessageModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# GET /api/message/{chat_id}
@router.get("/by_chat/{chat_id}", response_model=MessageListSchema)
def get_Message(chat_id: int, session: Session = Depends(get_session)): 
    query = select(MessageModel).where(MessageModel.chatId == chat_id).order_by(MessageModel.messageId)
    results = session.exec(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {"results": results, "count": len(results)}


# GET /api/message/{message_id}
@router.get("/by_message/{message_id}", response_model=MessageModel)
def get_Message(message_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(MessageModel).where(MessageModel.messageId == message_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Message not found")
    return result