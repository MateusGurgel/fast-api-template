import alembic.config
from alembic import command
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.databases.main.database import get_db


def create_database_engine():
    return create_engine(config("TEST_DATABASE_URL"))


def override_api_database(app):
    engine = create_database_engine()

    def override_get_db():
        try:
            db = get_database_session(engine)
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db


def get_database_session(engine):
    with engine.begin() as connection:
        migrate_db(connection=connection)

    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = session_maker()

    return session


def migrate_db(alembic_ini_path="alembic.ini", connection=None, revision="head"):
    config = alembic.config.Config(alembic_ini_path)

    if connection is None:
        return

    config.config_ini_section = "test-database"
    command.upgrade(config, revision)
