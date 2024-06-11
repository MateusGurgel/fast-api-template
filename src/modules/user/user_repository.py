from sqlalchemy.orm import Session

from src.modules.shared.base_repository import BaseRepository
from src.modules.user.user import User
from src.modules.user.user_schemas import CreateUserSchema
from src.utils.encryption import get_password_hash

from src.exceptions.resource_not_found import ResourceNotFound


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_id(self, user_id: int, db: Session):
        return self.select_first({"id": user_id}, db)

    def delete_user_by_id(self, id: str, db: Session) -> int:
        return self.delete_by_id(id, db)

    def get_user_by_username(self, username: str, db: Session):
        return self.select_first({"username": username}, db)

    def get_user_by_email(self, email: str, db: Session):
        return self.select_first({"email": email}, db)
    
    def does_email_exist(self, email: str, db: Session) -> bool:
        try:
            self.get_user_by_email(email, db)
            return True
        except ResourceNotFound:
            return False
    
    def create_user(self, user: CreateUserSchema, db: Session) -> CreateUserSchema:
        hashedPassword = get_password_hash(user.password)
        user.password = hashedPassword
        return self.insert(user, db)
    
user_repository = UserRepository()