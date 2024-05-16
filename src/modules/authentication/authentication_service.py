from exceptions.invalid_token_exception import invalid_token_exception
from exceptions.credential_exception import credentials_exception
from datetime import datetime, timedelta, timezone
from src.utils.encryption import verify_password
from src.modules.user import user_repository
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Union
import os


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_ENCRYPTION_ALGORITHM = os.getenv("ACCESS_TOKEN_ENCRYPTION_ALGORITHM")


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
    payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ENCRYPTION_ALGORITHM])
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
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ENCRYPTION_ALGORITHM)
    return encoded_jwt


def check_credentials(username: str, password, db: Session):
    user = user_repository.get_user_by_username(username, db)

    if not user:
        return False

    return verify_password(password, user.password)
