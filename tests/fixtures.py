import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from main import app
from tests.utils.database_utils import (
    create_database_engine,
    get_database_session,
    override_api_database,
)
from tests.utils.docker_utils import start_test_database_container

load_dotenv()


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session", autouse=True)
def override_api_database_fixture():
    override_api_database(app)


@pytest.fixture(scope="session", autouse=True)
def db_container():
    container = start_test_database_container()

    yield container

    container.stop()


@pytest.fixture(scope="session", autouse=True)
def db_session(db_container):

    engine = create_database_engine()
    session = get_database_session(engine)

    override_api_database(app)

    yield session

    session.close()
    engine.dispose()
