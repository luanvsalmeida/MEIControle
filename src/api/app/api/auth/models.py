from datetime import datetime, timezone
from typing import List, Optional
from pydantic import constr, EmailStr
import sqlmodel
from sqlmodel import SQLModel, Field

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

"""
+---------------- USER-----------------+
|   userId  |    pk (int)   | required |
+-----------|---------------|----------|
|   email   |     mail      | required |
+-----------|---------------|----------|
| username  |     string    | required |
+-----------|---------------|----------|
| password  | string (hash) | required |
+-----------|---------------|----------|
| business  |     string    | optional |
+-----------|---------------|----------|
| createdAt |    datetime   | auto-gen |
+--------------------------------------+
"""
class UserModel(SQLModel, table=True):
    userId: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)       # password needs to be hashed before
    business: Optional[str] = Field(default=None)
    created_at: datetime = Field(
    default_factory=get_utc_now,
    sa_type=sqlmodel.DateTime(timezone=True),
    nullable=False
    )

class UserCreateSchema(SQLModel):
    username: constr(min_length=3, max_length=40)
    email: constr(min_length=3, max_length=40) #EmailStr
    password: constr(min_length=6, max_length=25)
    business: Optional[str] = Field(default="")

class UserUpdateSchema(SQLModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None
    business: Optional[str] = None

# {"id": 12}

class UserListSchema(SQLModel):
    results: List[UserModel]
    count: int

class UserSignInSchema(SQLModel):
    email: EmailStr
    password: constr(min_length=6, max_length=25)
