from datetime import datetime
from typing import List, Optional
from pydantic import constr 
import sqlmodel 
from sqlmodel import SQLModel, Field
from timescaledb.utils import get_utc_now


"""
| Campo            | Tipo     | Obrigatório | Notas                    |
| ---------------- | -------- | ----------- | ------------------------ |
| `subscriptionId` | PK       | ✅          |                          |
| `userId`         | FK       | ✅          |                          |
| `plan`           | string   | ✅          | “Gratuito”, “Premium”    |
| `status`         | string   | ✅          | “Ativo”, “Cancelado”     |
| `startDate`      | datetime | ✅          |                          |
| `endDate`        | datetime | opcional    | Para planos com validade  |
"""

class SubscriptionModel(SQLModel, table=True):
    subscriptionId: Optional[int] = Field(default=None, primary_key=True)
    userId: int = Field(nullable=False, foreign_key="usermodel.userId")
    plan: str = Field(default=None)
    status: str = Field(nullable=False)
    startDate: datetime = Field(
        default=None,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=True
    )
    endDate: Optional[datetime] = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False 
    )
    
    
class SubscriptionCreateSchema(SQLModel):
    userId: int
    plan: constr(min_length=2, max_length=30)
    status: constr(min_length=2, max_length=30)
    endDate: Optional[datetime]

class SubscriptionUpdateSchema(SQLModel):
    plan: constr(min_length=2, max_length=30)
    status: constr(min_length=2, max_length=30)
    endDate: Optional[datetime]

class SubscriptionListSchema(SQLModel):
    results: List[SubscriptionModel]
    count: int 