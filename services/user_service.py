from schematics.user_schema import CreateUserSchema
from sqlalchemy.orm import Session
from repositories import user_repository as repository


def create_user(user: CreateUserSchema, db: Session) -> CreateUserSchema:
    return repository.create_user(user, db)
