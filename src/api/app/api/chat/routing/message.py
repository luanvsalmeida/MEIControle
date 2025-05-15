from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api.flows.routing.inflow import send_inflow as inflow_handler
from api.flows.routing.outflow import send_outflow as outflow_handler
from api.flows.models.inflow import InflowCreateSchema
from api.flows.models.outflow import OutflowCreateSchema
from api.chat.models.chat import ChatModel
from timescaledb.utils import get_utc_now


from api.db.session import get_session
from api.services.nlp.interpreter import interpretar_mensagem

from api.chat.models.message import (
    MessageModel,
    MessageCreateSchema,
    MessageListSchema
)

router = APIRouter()
from api.db.config import DATABASE_URL

@router.post("/", response_model=MessageModel)
def send_message(payload: MessageCreateSchema, session: Session = Depends(get_session)):
    texto = payload.content
    result = interpretar_mensagem(texto)
    print(result)

    # Get userId from chatId
    chat = session.exec(select(ChatModel).where(ChatModel.chatId == payload.chatId)).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    user_id = chat.userId

    # Message storing
    data = payload.model_dump()
    obj = MessageModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    print(obj)

    # Create (inflow)
    if result.get("operation") == "inflow":
        inflow_data = InflowCreateSchema(
            userId=user_id,
            value=result.get("value"),
            product=result.get("product"),
            date=get_utc_now()
        )
        inflow_handler(inflow_data, session)

    # Create (outflow)
    elif result.get("operation") == "outflow":
        outflow_data = OutflowCreateSchema(
            userId=user_id,
            value=result.get("value"),
            product=result.get("product"),
            date=get_utc_now()
        )
        outflow_handler(outflow_data, session)

    return obj  # Standard return (Need to be checked)


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