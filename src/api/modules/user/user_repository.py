from sqlalchemy.orm import Session

from src.api.modules.shared.base_repository import BaseRepository
from src.api.modules.user.user import User
from src.api.modules.user.user_schemas import CreateUserSchema
from src.api.utils.encryption import get_password_hash

from src.api.exceptions.resource_not_found import ResourceNotFound


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def search_by_id(self, id: str, db: Session):
        pass

    def search_by_username(self, username: str, db: Session):
        pass

    def search_by_email(self, email: str, db: Session):
        pass

    def does_email_exist(self, email: str, db: Session) -> bool:
        try:
            self.search_by_email(email, db)
            return True
        except ResourceNotFound:
            return False

    def create_user(self, user: CreateUserSchema, db: Session) -> CreateUserSchema:
        hashedPassword = get_password_hash(user.password)
        user.password = hashedPassword
        return self.insert(user, db)


user_repository = UserRepository()
