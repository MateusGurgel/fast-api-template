import textwrap
from types import MethodType
from typing import List

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from src.exceptions.resource_not_found import ResourceNotFound


class BaseRepository:
    def __init__(self, base_model: DeclarativeMeta):
        self.base_model = base_model
        self.__search_function_prefix = "search_by_"
        self.__generate_search_functions()

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

    def insert(self, pydantc_model: PydanticBaseModel, db: Session):
        """
        Inserts a new record into the database.

        Args:
            pydantc_model (PydanticBaseModel): The Pydantic model representing the data to be inserted.
            db (Session): The database session.

        Returns:
            The inserted database model.
        """

        db_model = self.base_model(**pydantc_model.model_dump())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    def insert_many(self, pydantc_models: List[PydanticBaseModel], db: Session):
        """
        Inserts multiple Pydantic models into the database.

        Args:
            pydantc_models (List[PydanticBaseModel]): A list of Pydantic models to be inserted.
            db (Session): The database session.

        Returns:
            List[BaseModel]: A list of the inserted database models.
        """

        db_models = []

        for pydantic_model in pydantc_models:
            db_model = self.base_model(**pydantic_model.model_dump())
            db_models.append(db_model)

        db.add_all(db_models)
        db.commit()

        for db_model in db_models:
            db.refresh(db_model)

        return db_models

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

    def __generate_search_functions(self):
        function_names = self.__get_class_function_names()

        for function_name in function_names:
            if not self.__is_search_function_name(function_name):
                continue

            sulfix: str = self.__get_search_function_sulfix(function_name)

            search_function = self.__generate_search_function(function_name, sulfix)

            self.__add_search_function(function_name, search_function)

    def __add_search_function(self, function_name: str, search_function: MethodType):
        setattr(self, function_name, search_function)

    def __generate_search_function(self, function_name: str, sulfix: str):
        search_function_text: str = self.__assemble_search_function(
            function_name, sulfix
        )
        exec(search_function_text)
        search_function = MethodType(locals()[function_name], self)
        return search_function

    def __assemble_search_function(self, function_name, sulfix):
        function: str = textwrap.dedent(
            f"""
        def {function_name}(self, {sulfix}: str, db):
            where = {{"{sulfix}": {sulfix}}}
            return self.select_first(where, db)
        """
        )
        return function

    def __is_search_function_name(self, function_name):
        return function_name.startswith(self.__search_function_prefix)

    def __get_search_function_sulfix(self, function_name):
        return function_name[len(self.__search_function_prefix) :]

    def __get_class_function_names(self):
        functions = [
            attr
            for attr in dir(self)
            if callable(getattr(self, attr)) and not attr.startswith("__")
        ]
        return functions
