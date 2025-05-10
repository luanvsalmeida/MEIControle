from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import JSON
from pydantic import constr 
import sqlmodel 
from sqlmodel import SQLModel, Field

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

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
|    tokens    |     str []    | optional |
+--------------|---------------|----------|
|      date    |    datetime   | auto-gen |
+-----------------------------------------+
"""

class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class MessageModel(SQLModel, table=True):
    messageId: Optional[int] = Field(default=None, primary_key=True)
    chatID: int = Field(nullable=False, foreign_key="chat.chatId")
    role: RoleEnum = Field(nullable=False, index=True)
    content: str = Field(nullable=False) 
    tokens: Optional[List[str]] = Field(default=None, sa_type=JSON)
    date: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.sql.sqltypes.DateTime(timezone=True),
        nullable=False
    )

class MessageCreateSchema(SQLModel):
    chatID: int
    role: RoleEnum
    content: constr(max_length=1000)
    tokens: Optional[List[str]] = None
