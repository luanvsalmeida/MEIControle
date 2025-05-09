import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


from api.db.session import get_session

from .models import (
    UserModel,
    UserListSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserSignInSchema
)
router  = APIRouter()
from api.db.config import DATABASE_URL

# POST/api/signup
def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/signup", response_model=UserModel)
def create_user(payload: UserCreateSchema, session: Session = Depends(get_session)): 
    data = payload.model_dump()
    data["password"] = hash_password(data["password"])
    obj = UserModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj



# POST/api/signin
@router.post("/signin")
def signin(payload: UserSignInSchema, session: Session = Depends(get_session)):
    user = session.exec(select(UserModel).where(UserModel.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"sub": str(user.userId)}  # or user.email
    token = create_access_token(data=token_data)
    
    return {"access_token": token, "token_type": "bearer"}

# /logout (if it would have a blacklist, like redis)

# /delete-account

# /edit-account
@router.put("/{user_id}", response_model=UserModel)
def edit_account(user_id: int,
                 payload: UserUpdateSchema,
                 session: Session = Depends(get_session)):
    query = select(UserModel).where(UserModel.userId == user_id)
    obj = session.exc(query).first()
    if not obj: 
        raise HTTPException(status_code=404, detail="User not found")

    data = payload.model_dump()

    for k, v in data.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj
 
# GET/api/Users/
"""
@router.get("/{User_id}", response_model=UserModel)
def get_User(User_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(UserModel).where(UserModel.id == User_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


    """