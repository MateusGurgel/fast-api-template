from fastapi import Depends
from typing_extensions import Annotated
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from repositories import user_repository
from services.authentication_service import try_get_user_username_from_token

from fastapi.security import OAuth2PasswordBearer

Oauth2 = OAuth2PasswordBearer(tokenUrl="Bearer")


async def get_current_user(
    token: Annotated[str, Depends(Oauth2)], db: Annotated[Session, Depends(get_db)]
) -> User:
    username = try_get_user_username_from_token(token)
    user = user_repository.get_user_by_username(username, db)
    return user


token = Annotated[str, Depends(Oauth2)]
database = Annotated[Session, Depends(get_db)]
current_user = Annotated[User, Depends(get_current_user)]
