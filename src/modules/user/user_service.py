from src.modules.user.user_schemas import CreateUserSchema
from sqlalchemy.orm import Session
from src.modules.user import user_repository as repository


def create_user(user: CreateUserSchema, db: Session) -> CreateUserSchema:
    return repository.create_user(user, db)
