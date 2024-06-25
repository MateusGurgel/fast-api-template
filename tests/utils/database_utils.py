import alembic.config
from alembic import command
from decouple import config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.databases.main.database import get_db


def override_api_database(session_maker, app):
    def override_get_db():
        try:
            session = session_maker()
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db


def create_database_engine():
    return create_engine(config("TEST_DATABASE_URL"))


def get_database_session_maker(engine):
    with engine.begin() as connection:
        migrate_db(connection=connection)

    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return session_maker


def delete_data(session: Session):

    meta = MetaData()
    meta.reflect(bind=session.bind)

    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())

    session.commit()


def migrate_db(alembic_ini_path="alembic.ini", connection=None, revision="head"):

    config = alembic.config.Config(alembic_ini_path)

    if connection is None:
        return

    config.config_ini_section = "test-database"
    command.upgrade(config, revision)
