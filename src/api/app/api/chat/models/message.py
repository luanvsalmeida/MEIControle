# api/chat/models/message.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import JSON
from pydantic import constr 
import sqlmodel 
from sqlmodel import SQLModel, Field
from timescaledb.utils import get_utc_now

"""
+----------------- MESSAGE ---------------+
|   messageId  |    pk (int)   | required |
+--------------|---------------|----------|
|    chatID    |     fk (int)  | required |
+--------------|---------------|----------|
|     role     |      enum     | required |
+--------------|---------------|----------|
|    content   |      str      | required |
+--------------|---------------|----------|
|    message   |      str      | optional | -> User message content
+--------------|---------------|----------|
|     chart    |      str      | optional | -> Path to chart file
+--------------|---------------|----------|
|    report    |      str      | optional | -> Path to report file
+--------------|---------------|----------|
|    tokens    |     str []    | optional |
+--------------|---------------|----------|
|      date    |    datetime   | auto-gen |
+-----------------------------------------+

tokens will be something like:

{
    "operation": "inflow"/"outflow"/"report"/"forecast" -> it will define the routing
    "value": "50.00"(in case of in/outflow)/"start-end (a date period in case of report or forecast)
    "item": "bebidas" (in/outflow)/"pdf", "csv", etc. (report)/"sells" (forecast)
}
"""

class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class MessageModel(SQLModel, table=True):
    messageId: Optional[int] = Field(default=None, primary_key=True)
    chatId: int = Field(nullable=False, foreign_key="chatmodel.chatId")
    role: RoleEnum = Field(nullable=False, index=True)
    content: str = Field(nullable=False)  # Main content field (backward compatibility)
    message: Optional[str] = Field(default=None)  # Separate message field
    chart: Optional[str] = Field(default=None)    # Path to chart file
    report: Optional[str] = Field(default=None)   # Path to report file
    tokens: Optional[List[str]] = Field(default=None, sa_type=JSON)
    date: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

class MessageCreateSchema(SQLModel):
    chatId: int
    role: RoleEnum
    content: constr(max_length=1000)
    message: Optional[str] = None
    chart: Optional[str] = None
    report: Optional[str] = None
    tokens: Optional[List[str]] = None

class MessageListSchema(SQLModel):
    results: List[MessageModel]
    count: int