# api/flows/models/outflow.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import constr 
import sqlmodel 
from sqlmodel import SQLModel, Field
from timescaledb.utils import get_utc_now

"""
| Campo         | Tipo     | Obrigatório | Notas              |
| ------------- | -------- | ----------- | ------------------ |
| `purchaseId`  | PK       | ✅           |                    |
| `userId`      | FK       | ✅           |                    |
| `supplier`    | string   | opcional    | OK manter opcional |
| `value`       | float    | ✅           |                    |
| `date`        | datetime | ✅           |                    |
| `type`        | enum     | ✅           |                    |
| `paymentForm` | enum     | opcional    |                    |
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

class OutflowModel(SQLModel, table=True):
    outflowId: Optional[int] = Field(default=None, primary_key=True)
    userId: int = Field(nullable=False, foreign_key="usermodel.userId")
    supplier: Optional[str] = Field(default=None)
    value: float = Field(nullable=False)
    product: str = Field(nullable=False)
    date: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False 
    )
    type: Optional[TypeEnum] = Field(default=None, index=True)
    paymentForm: Optional[PaymentEnum] = Field(default=None, index=True)
    
class OutflowCreateSchema(SQLModel):
    userId: int
    supplier: Optional[constr(max_length=50)] = None
    product: constr(max_length=100)
    value: float 
    type: Optional[TypeEnum] = None
    paymentForm: Optional[PaymentEnum] = None
    date: Optional[datetime] = None  

class OutflowListSchema(SQLModel):
    results: List[OutflowModel]
    count: int 