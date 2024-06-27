from datetime import datetime, timedelta, timezone
from typing import Union

from decouple import config
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.api.exceptions.credential_exception import credentialsException
from src.api.exceptions.invalid_token_exception import InvalidTokenException
from src.api.modules.user.user_repository import user_repository
from src.api.utils.encryption import verify_password

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
ACCESS_TOKEN_SECRET_KEY = config("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_ENCRYPTION_ALGORITHM = config("ACCESS_TOKEN_ENCRYPTION_ALGORITHM")


def authenticate(username: str, password, db: Session) -> str:
    if not check_credentials(username, password, db):
        raise credentialsException

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": username}, access_token_expires)

    return token


def try_get_user_username_from_token(token: str) -> str:
    try:
        return get_user_username_from_token(token)
    except JWTError:
        raise InvalidTokenException


def get_user_username_from_token(token: str) -> str:
    payload = jwt.decode(
        token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ENCRYPTION_ALGORITHM]
    )
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
    encoded_jwt = jwt.encode(
        to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ENCRYPTION_ALGORITHM
    )
    return encoded_jwt


def check_credentials(username: str, password, db: Session):
    user = user_repository.search_by_username(username, db)

    if not user:
        return False

    return verify_password(password, user.password)
