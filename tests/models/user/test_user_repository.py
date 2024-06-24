from src.modules.user.user_repository import UserRepository
from src.modules.user.user_schemas import CreateUserSchema


def test_create_user(db_session):
    user_repository = UserRepository()

    user = {
        "username": "test_user",
        "email": "example@example.com",
        "password": "test_password",
    }

    user = CreateUserSchema(**user)

    user = user_repository.create_user(user, db_session)

    assert user is not None
    assert user.id is not None
    assert user.username == "test_user"
    assert user.email == "example@example.com"
