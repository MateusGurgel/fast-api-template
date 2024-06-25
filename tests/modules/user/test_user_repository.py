from src.modules.user.user_repository import UserRepository
from src.modules.user.user_schemas import CreateUserSchema


def get_mock_user():
    user = {
        "username": "test_user",
        "email": "example@example.com",
        "password": "test_password",
    }

    return user


def test_create_user(db_session):
    user_repository = UserRepository()

    user = get_mock_user()

    persisted_user = CreateUserSchema(**user)

    persisted_user = user_repository.create_user(persisted_user, db_session)

    assert persisted_user is not None
    assert persisted_user.id is not None
    assert persisted_user.username == "test_user"
    assert persisted_user.email == "example@example.com"


def test_select_user_by_id(db_session):
    user_repository = UserRepository()

    user = get_mock_user()

    persisted_user = user_repository.search_by_id(1, db_session)

    assert persisted_user is None
