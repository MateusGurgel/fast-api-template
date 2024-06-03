from src.exceptions.email_already_used_exception import EmailAlreadyUsedException
from src.modules.user.user_schemas import CreateUserSchema
from sqlalchemy.orm import Session
from src.modules.user.user_repository import user_repository as repository


def create_user(user: CreateUserSchema, db: Session) -> CreateUserSchema:

    if repository.get_user_by_email(user.email, db):
        raise EmailAlreadyUsedException()

    return repository.create_user(user, db)
