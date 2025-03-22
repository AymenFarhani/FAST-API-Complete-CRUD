from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel

from models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "1365eg65885g5rgv56654ef6rg54erg5erg15erg5eg"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
  username: str
  password: str

class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username, password, db):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id, expires_delta: timedelta):
    encode = {'sub':username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):
    try:
        payload: jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if not username or not user_id:
            raise HTTPException(status_code=401, detail="Could not verify user.")
        return {'username': username, 'id': user_id}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")



