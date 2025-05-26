# api/chat/models/chat.py
from datetime import datetime, timezone 
from typing import List, Optional 
from sqlalchemy import JSON
import sqlmodel 
from sqlmodel import SQLModel, Field
from timescaledb.utils import get_utc_now

"""
|  Field    | Tipo       | Obrigatório | Notas                    |
| --------- | ---------- | ----------- | ------------------------ |
| `chatID`  | PK         | ✅          |                          |
| `userID`  | FK         | ✅          |                          |
| `date`    | datetime   | ✅          | Início do chat           |
| `context` | JSON/text? | opcional    | Tokens do histórico/chat |

"""

class ChatModel(SQLModel, table=True):
    chatId: Optional[int] = Field(default=None, primary_key=True)
    userId: int = Field(nullable=False, foreign_key="usermodel.userId")
    context: Optional[List[str]] = Field(default=None, sa_type=JSON)
    date: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

class ChatCreateSchema(SQLModel):
    userId: int 
    context: Optional[List[str]] = None

class ChatListSchema(SQLModel):
    results: List[ChatModel]
    count: int 


    