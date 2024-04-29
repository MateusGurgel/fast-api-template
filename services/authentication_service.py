from exceptions.invalid_token_exception import invalid_token_exception
from exceptions.credential_exception import credentials_exception
from datetime import datetime, timedelta, timezone
from services.encryption_service import verify_password
from repositories import user_repository
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Union
import os


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def authenticate(username: str, password, db: Session) -> str:

    if not check_credentials(username, password, db):
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": username}, access_token_expires)

    return token


def try_get_user_username_from_token(token: str) -> str:
    try:
        return get_user_username_from_token(token)
    except JWTError:
        raise invalid_token_exception


def get_user_username_from_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")

    if not username:
        raise JWTError
    return username


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_credentials(username: str, password, db: Session):
    user = user_repository.get_user_by_username(username, db)

    if not user:
        return False

    return verify_password(password, user.password)
