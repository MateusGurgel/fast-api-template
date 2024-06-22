import alembic.config
from alembic import command


def migrate_to_db(alembic_ini_path="alembic.ini", connection=None, revision="head"):
    config = alembic.config.Config(alembic_ini_path)

    if connection is None:
        return

    config.config_ini_section = "test-database"
    command.upgrade(config, revision)
