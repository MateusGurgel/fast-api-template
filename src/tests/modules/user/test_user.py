import pytest

from src.api.exceptions.resource_not_found import ResourceNotFound
from src.api.modules.user.user_repository import UserRepository
from src.api.modules.user.user_schemas import UserCreateSchema
from src.api.modules.user.user_service import create_user
from src.api.utils.encryption import verify_password


def get_mock_user():
    return UserCreateSchema(
        **{
            "username": "test_user",
            "password": "test_password",
            "email": "example@example.com",
        }
    )


def create_mock_user(db_session, user=get_mock_user()):
    persisted_user = create_user(user, db_session)

    return persisted_user


def test_user_login(client, db_session):

    mock_user = get_mock_user()

    create_mock_user(db_session, mock_user.model_copy())

    response = client.post(
        "/Bearer",
        data={"username": mock_user.username, "password": mock_user.password},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_self_delete(client, db_session):
    userRepository = UserRepository()

    mock_user = get_mock_user()

    persisted_user = create_mock_user(db_session, mock_user.model_copy())

    login_response = client.post(
        "/Bearer",
        data={"username": mock_user.username, "password": mock_user.password},
    )

    bearer_token = login_response.json()["access_token"]

    response = client.delete(
        "/users/me", headers={"Authorization": f"Bearer {bearer_token}"}
    )

    assert response.status_code == 200

    with pytest.raises(ResourceNotFound):
        userRepository.search_by_id(persisted_user.id, db_session)


def test_create_user(client, db_session):

    user_repository = UserRepository()

    user = get_mock_user()

    response = client.post("/users", json=user.model_dump())

    assert response.status_code == 201

    persisted_user = user_repository.search_by_id(response.json()["id"], db_session)

    assert persisted_user is not None
    assert persisted_user.username == user.username
    assert persisted_user.email == user.email
    assert verify_password(user.password, persisted_user.password)
