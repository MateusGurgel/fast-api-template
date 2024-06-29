import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from main import app
from src.databases.redis.redis_client import redis_client
from src.databases.test.database import (
    create_database_engine,
    delete_data,
    get_database_session_maker,
    override_api_database,
)
from src.tests.utils.docker.postgres_test_container import postgree_test_container
from src.tests.utils.docker.redis_test_container import redis_test_container

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def redis_container():
    container = redis_test_container.start()

    redis_client.set_client(port=6380)

    yield container

    container.stop()


@pytest.fixture(scope="session", autouse=True)
def db_container():
    container = postgree_test_container.start()

    yield container

    container.stop()


@pytest.fixture(autouse=True)
def reset_redis(redis_container):
    redis_client.flushdb()


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
