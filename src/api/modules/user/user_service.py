from sqlalchemy.orm import Session

from src.api.core.exceptions.email_already_used_exception import EmailAlreadyUsedException
from src.api.modules.user.user_repository import user_repository as repository
from src.api.modules.user.user_schemas import UserCreateSchema
from src.api.core.utils.encryption import get_password_hash


def create_user(user: UserCreateSchema, db: Session) -> UserCreateSchema:

    if repository.does_email_exist(user.email, db):
        raise EmailAlreadyUsedException()

    user.password = get_password_hash(user.password)

    return repository.create_user(user, db)


def search_by_id(user_id, db: Session):
    return repository.search_by_id(user_id, db)


def delete_user_by_id(user_id, db: Session):
    return repository.delete_by_id(user_id, db)


def search_by_username(username: str, db: Session):
    return repository.search_by_username(username, db)
