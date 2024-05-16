from fastapi import APIRouter
from src.modules.user.user_schemas import CreateUserSchema, UserListSchema
from src.modules.user import user_service
from src.modules.shared.dependencies import current_user
from src.modules.shared.dependencies import current_user, database


user_router = APIRouter(prefix=("/users"), tags=["user"])


@user_router.post("/", summary="Create a new user")
async def create_user(user: CreateUserSchema, db: database):
    user = user_service.create_user(user, db)
    return user


@user_router.get("/me", summary="Get current user")
async def get_current_user(user: current_user) -> UserListSchema:
    return user
