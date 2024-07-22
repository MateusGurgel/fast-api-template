from typing import List

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from src.api.core.exceptions.resource_not_found import ResourceNotFound


class BaseRepository:
    def __init__(self, base_model: DeclarativeMeta):
        self.base_model = base_model

    def select(self, where: dict, db: Session):
        """Select records from the database based on the given conditions.

        Args:
            where (dict): A dictionary specifying the conditions for the selection.
            db (Session): The database session object.

        Returns:
            Query: A SQLAlchemy query object representing the selected records.
        """

        return db.query(self.base_model).filter_by(**where)

    def select_first(self, where: dict, db: Session):
        """
        Selects and returns the first record from the database that matches the given conditions.

        Args:
            where (dict): A dictionary representing the conditions to filter the records.
            db (Session): The database session.

        Returns:
            The first record that matches the given conditions, or None if no record is found.
        """

        query = db.query(self.base_model).filter_by(**where).first()

        if not query:
            raise ResourceNotFound()

        return query

    def create(self, model: DeclarativeMeta, db: Session):
        """
        Inserts a new record into the database.

        Args:
            pydantc_model (DeclarativeMeta): The Pydantic model representing the data to be inserted.
            db (Session): The database session.

        Returns:
            The inserted database model.
        """

        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    def create_many(self, models: List[DeclarativeMeta], db: Session):
        """
        Inserts multiple Pydantic models into the database.

        Args:
            models (List[DeclarativeMeta]): A list of models to be inserted.
            db (Session): The database session.

        Returns:
            List[BaseModel]: A list of the inserted database models.
        """

        db.add_all(models)
        db.commit()

        for model in models:
            db.refresh(model)

        return models

    def delete_by_id(self, id: str, db: Session) -> int:
        """
        Deletes a record from the database based on the given ID.

        Args:
            id (str): The ID of the record to be deleted.
            db (Session): The database session.

        Returns:
            int: The number of records deleted.
        """
        return self.delete({"id": id}, db)

    def delete(self, where: dict, db: Session) -> int:
        """
        Deletes records from the database based on the given conditions.

        Args:
            where (dict): A dictionary specifying the conditions for deletion.
            db (Session): The database session.

        Returns:
            int: The number of records deleted.
        """

        query = self.select(where, db)
        deleted_rows = query.delete()
        db.commit()
        return deleted_rows
