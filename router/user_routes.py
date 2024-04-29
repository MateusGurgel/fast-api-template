from fastapi import APIRouter, Depends
from database import get_db
from schematics.user_schema import CreateUserSchema
from services import user_service
from sqlalchemy.orm import Session


user_router = APIRouter(prefix=("/users"), tags=["users"])


@user_router.post("/", summary="Create a new user")
async def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    user = user_service.create_user(user, db)
    return user
