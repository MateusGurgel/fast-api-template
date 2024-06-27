from fastapi import APIRouter

from src.api.modules.shared.dependencies import current_user, database
from src.api.modules.user import user_service
from src.api.modules.user.user_schemas import UserCreateSchema, UserListSchema

user_router = APIRouter(prefix=("/users"), tags=["user"])


@user_router.post("/", summary="Create a new user", status_code=201)
async def create_user(user: UserCreateSchema, db: database):
    user = user_service.create_user(user, db)
    return user


@user_router.get("/me", summary="Get current user")
async def get_current_user(user: current_user) -> UserListSchema:
    return user


@user_router.delete("/me", summary="Delete current user")
async def delete_current_user(user: current_user, db: database):
    return user_service.delete_user_by_id(user.id, db)
