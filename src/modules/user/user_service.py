from sqlalchemy.orm import Session

from src.exceptions.email_already_used_exception import EmailAlreadyUsedException
from src.modules.user.user_repository import user_repository as repository
from src.modules.user.user_schemas import CreateUserSchema


def create_user(user: CreateUserSchema, db: Session) -> CreateUserSchema:

    if repository.does_email_exist(user.email, db):
        raise EmailAlreadyUsedException()

    return repository.create_user(user, db)

def get_user_by_id(user_id: int, db: Session):
    return repository.get_user_by_id(user_id, db)

def delete_user_by_id(user_id: int, db: Session):
    return repository.delete_user_by_id(user_id, db)

def get_user_by_username(username: str, db: Session):
    return repository.get_user_by_username(username, db)