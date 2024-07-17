from sqlalchemy.orm import Session

from src.api.core.exceptions.resource_not_found import ResourceNotFound
from src.api.core.base_repository import BaseRepository
from src.api.modules.user.user import User
from src.api.modules.user.user_schemas import UserCreateSchema


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def search_by_id(self, id: str, db: Session):
        return self.select_first({"id": id}, db)

    def search_by_username(self, username: str, db: Session):
        return self.select_first({"username": username}, db)

    def search_by_email(self, email: str, db: Session):
        return self.select_first({"email": email}, db)

    def does_email_exist(self, email: str, db: Session) -> bool:
        try:
            self.search_by_email(email, db)
            return True
        except ResourceNotFound:
            return False

    def create_user(self, user: UserCreateSchema, db: Session) -> UserCreateSchema:
        return self.insert(user, db)


user_repository = UserRepository()
