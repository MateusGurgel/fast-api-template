from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.modules.shared.dependencies import current_user, database
from src.modules.authentication import authentication_service
from src.modules.authentication.token_schema import Token


auth_router = APIRouter()


@auth_router.post("/Bearer", summary="Login")
async def get_bearer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: database
):
    token = authentication_service.authenticate(
        form_data.username, form_data.password, db
    )
    return Token(access_token=token, token_type="bearer")


@auth_router.post("/Test-bearer", summary="Test Login")
async def test_bearer(user: current_user):
    return "ok"
