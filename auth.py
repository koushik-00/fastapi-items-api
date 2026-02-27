from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

import os
from dotenv import load_dotenv
load_dotenv()



pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password) -> str:
    # takes a plain password, returns a hashed version using passlib
    return pwd_context.hash(password[:72])

def verify_password(plain_password, hashed_password) -> bool:
    # returns True or False
    return pwd_context.verify(plain_password[:72], hashed_password)

SECRET_KEY = os.getenv('SECRET_KEY')
EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

