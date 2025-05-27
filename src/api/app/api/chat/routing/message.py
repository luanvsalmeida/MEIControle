# api/chat/routing/message.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api.flows.routing.inflow import send_inflow as inflow_handler
from api.flows.routing.outflow import send_outflow as outflow_handler
from api.events.handlers.forecast import get_forecast as forecast_handler
from api.events.handlers.chart import generate_chart as chart_handler
from api.flows.models.inflow import InflowCreateSchema
from api.flows.models.outflow import OutflowCreateSchema
from api.chat.models.chat import ChatModel
from api.services.ai.chatgpt_client import gpt_answer
from timescaledb.utils import get_utc_now
from pathlib import Path
import json

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
    """
    Process user message and execute corresponding operations
    
    Args:
        payload: Message data from user
        session: Database session
        
    Returns:
        MessageModel with response content and file paths
    """
    
    texto = payload.content
    result = interpretar_mensagem(texto)
    print(f"NLP Result: {result}")

    # Get userId from chatId
    chat = session.exec(select(ChatModel).where(ChatModel.chatId == payload.chatId)).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    user_id = chat.userId

    # Initialize message object
    data = payload.model_dump()
    obj = MessageModel.model_validate(data)
    
    # Initialize response fields
    response_message = ""
    chart_path = None
    report_path = None

    # Process different operations
    if result.get("operation") == "inflow":
        # Handle inflow creation
        inflow_data = InflowCreateSchema(
            userId=user_id,
            value=result.get("value"),
            product=result.get("product"),
            date=get_utc_now()
        )
        inflow_handler(inflow_data, session)
        response_message = f'Venda de R$ {result.get("value"):.2f} de {result.get("product")} registrada com sucesso'

    elif result.get("operation") == "outflow":
        # Handle outflow creation
        outflow_data = OutflowCreateSchema(
            userId=user_id,
            value=result.get("value"),
            product=result.get("product"),
            date=get_utc_now()
        )
        outflow_handler(outflow_data, session)
        response_message = f'Compra de R$ {result.get("value"):.2f} de {result.get("product")} registrada com sucesso'

    elif result.get("operation") == "forecast":
        # Handle forecast generation
        forecast = forecast_handler(user_id, session)
        response_message = forecast["mensagem"]
        print(f"Forecast message: {response_message}")

    elif result.get("operation") == "report":
        # Handle chart and report generation
        try:
            chart_data = chart_handler(user_id, session)
            
            # Validate chart_data structure
            if not isinstance(chart_data, dict):
                raise HTTPException(status_code=500, detail="Invalid chart data format")
            
            # Extract response components
            response_message = chart_data.get("message", "Relatório gerado com sucesso")
            chart_path = chart_data.get("chart")
            report_path = chart_data.get("report")
            
            print(f"Chart generated: {chart_path}")
            print(f"Report generated: {report_path}")
            
        except Exception as e:
            print(f"Error generating chart/report: {str(e)}")
            response_message = "Erro ao gerar relatório. Tente novamente."
            chart_path = None
            report_path = None

    elif result.get("operation") == "save":
        # Handle product saving
        label = result.get("label")
        if label:
            novo_produto = {"label": label, "type": "produto"}

            # Path to classification rules JSON
            file_path = Path(__file__).resolve().parent.parent.parent / "data" / "classificationRules.json"

            try:
                # Load existing products
                with open(file_path, "r", encoding="utf-8") as f:
                    produtos = json.load(f)

                # Add new product and save
                produtos.append(novo_produto)

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(produtos, f, indent=4, ensure_ascii=False)

                response_message = f"Produto '{label}' salvo com sucesso."
                
            except Exception as e:
                print(f"Error saving product: {str(e)}")
                response_message = "Erro ao salvar produto. Tente novamente."
        else:
            response_message = "Nome do produto não fornecido para salvamento."

    else:
        # Handle unrecognized operations        
        print("Operação não reconhecida. Enviando para o ChatGPT...")
        response_message = gpt_answer(texto)

    # Set response fields
    obj.content = response_message  # For backward compatibility
    obj.message = response_message
    obj.chart = chart_path
    obj.report = report_path
    
    # Save message to database
    session.add(obj)
    session.commit()
    session.refresh(obj)
    
    return obj


# GET /api/message/by_chat/{chat_id}
@router.get("/by_chat/{chat_id}", response_model=MessageListSchema)
def get_messages_by_chat(chat_id: int, session: Session = Depends(get_session)): 
    """
    Get all messages for a specific chat
    
    Args:
        chat_id: Chat ID to filter messages
        session: Database session
        
    Returns:
        List of messages for the chat
    """
    query = select(MessageModel).where(MessageModel.chatId == chat_id).order_by(MessageModel.messageId)
    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Messages not found for this chat")
    
    return {"results": results, "count": len(results)}


# GET /api/message/by_message/{message_id}
@router.get("/by_message/{message_id}", response_model=MessageModel)
def get_message_by_id(message_id: int, session: Session = Depends(get_session)): 
    """
    Get a specific message by ID
    
    Args:
        message_id: Message ID to retrieve
        session: Database session
        
    Returns:
        Single message object
    """
    query = select(MessageModel).where(MessageModel.messageId == message_id)
    result = session.exec(query).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return result