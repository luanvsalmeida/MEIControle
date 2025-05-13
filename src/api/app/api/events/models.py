from typing import List, Optional
from datetime import datetime
# from pydantic import BaseModel, Field
import sqlmodel
from sqlmodel import SQLModel, Field
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now


def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


# page visits at any given time
class EventModel(TimescaleModel, table=True):
    # id: Optional[int] = Field(default=None, primary_key=True)
    # id: int
    page: str = Field(index=True) # /about 
    description: Optional[str] = ""
    # created_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str


# {"id": 12}

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int