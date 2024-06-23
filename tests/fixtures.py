import pytest
from decouple import config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.utils.database_utils import migrate_to_db
from tests.utils.docker_utils import start_test_database_container

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_test_database_container()

    engine = create_engine(config("TEST_DATABASE_URL"))

    with engine.begin() as connection:
        migrate_to_db("alembic.ini", connection)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield SessionLocal()

    engine.dispose()
    container.stop()
