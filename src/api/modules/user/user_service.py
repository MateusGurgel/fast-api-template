from sqlalchemy.orm import Session

from src.api.exceptions.email_already_used_exception import EmailAlreadyUsedException
from src.api.modules.user.user_repository import user_repository as repository
from src.api.modules.user.user_schemas import CreateUserSchema


def create_user(user: CreateUserSchema, db: Session) -> CreateUserSchema:
    if repository.does_email_exist(user.email, db):
        raise EmailAlreadyUsedException()

    return repository.create_user(user, db)


def search_by_id(user_id, db: Session):
    return repository.search_by_id(user_id, db)


def delete_user_by_id(user_id, db: Session):
    return repository.delete_by_id(user_id, db)


def search_by_username(username: str, db: Session):
    return repository.search_by_username(username, db)
