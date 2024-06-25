import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from main import app
from tests.utils.database_utils import (
    create_database_engine,
    delete_data,
    get_database_session_maker,
    override_api_database,
)
from tests.utils.docker_utils import start_test_database_container

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def db_container():
    container = start_test_database_container()

    yield container

    container.stop()


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session", autouse=True)
def override_api_database_fixture(db_session_maker):
    override_api_database(db_session_maker, app)


@pytest.fixture(scope="session", autouse=True)
def db_session_maker():
    engine = create_database_engine()
    session_maker = get_database_session_maker(engine)

    yield session_maker

    engine.dispose()


@pytest.fixture
def db_session(db_session_maker):

    session = db_session_maker()

    delete_data(session)

    yield session

    session.rollback()
    session.close()
