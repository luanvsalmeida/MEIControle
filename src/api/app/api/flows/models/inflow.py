# api/flows/models/inflow.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import constr 
import sqlmodel 
from sqlmodel import SQLModel, Field
from timescaledb.utils import get_utc_now

"""
| Campo         | Tipo     | Obrigatório | Notas                     |
| ------------- | -------- | ----------- | ------------------------- |
| `saleId`      | PK       | ✅          |                           |
| `userId`      | FK       | ✅          |                           |
| `client`      | string   | opcional    | OK manter opcional        |
| `value`       | float    | ✅          |                           |
| `date`        | datetime | ✅          |                           |
| `product` | str      | ✅          |                           |
| `type`        | enum     | ✅          | “produto”, “serviço”, etc |
| `paymentForm` | enum     | opcional    | “pix”, “dinheiro”, etc    |
"""

class TypeEnum(str, Enum):
    unknow = "Não especificado",
    product = "produto",
    service = "serviço"

class PaymentEnum(str, Enum):
    unknow = "Não especificado",
    debit = "débito",
    credit = "crédito",
    cash = "dinheiro",
    pix = "pix"

class InflowModel(SQLModel, table=True):
    inflowId: Optional[int] = Field(default=None, primary_key=True)
    userId: int = Field(nullable=False, foreign_key="usermodel.userId")
    client: Optional[str] = Field(default=None)
    value: float = Field(nullable=False)
    product: str = Field(nullable=False)
    date: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False 
    )
    type: Optional[TypeEnum] = Field(default=None, index=True)
    paymentForm: Optional[PaymentEnum] = Field(default=None, index=True)

class InflowCreateSchema(SQLModel):
    userId: int
    client: Optional[constr(max_length=50)] = None
    product: constr(max_length=100)
    value: float 
    type: Optional[TypeEnum] = None
    paymentForm: Optional[PaymentEnum] = None
    date: Optional[datetime] = None  

class InflowListSchema(SQLModel):
    results: List[InflowModel]
    count: int 