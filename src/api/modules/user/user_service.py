from sqlalchemy.orm import Session

from src.api.core.exceptions.email_already_used_exception import (
    EmailAlreadyUsedException,
)
from src.api.core.logging import logger
from src.api.core.utils.encryption import get_password_hash
from src.api.modules.user.user import User
from src.api.modules.user.user_repository import user_repository as repository
from src.api.modules.user.user_schemas import UserCreateSchema


def create_user(user: UserCreateSchema, db: Session) -> UserCreateSchema:

    logger.info(f"Creating user with email: {user.email}")

    if repository.does_email_exist(user.email, db):
        raise EmailAlreadyUsedException()

    user.password = get_password_hash(user.password)

    user = User(**user.model_dump())

    return repository.create_user(user, db)


def search_by_id(user_id, db: Session):
    return repository.search_by_id(user_id, db)


def delete_user_by_id(user_id, db: Session):
    return repository.delete_by_id(user_id, db)


def search_by_username(username: str, db: Session):
    return repository.search_by_username(username, db)
