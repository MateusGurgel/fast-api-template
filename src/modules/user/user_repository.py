from sqlalchemy.orm import Session
from src.modules.user.user_schemas import CreateUserSchema
from src.modules.user.user import User
from src.utils.encryption import get_password_hash
from src.modules.shared.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_id(self, user_id: int, db: Session):
        return self.select_first({"id": user_id}, db)

    def get_user_by_username(self, username: str, db: Session):
        return self.select_first({"username": username}, db)

    def get_user_by_email(self, email: str, db: Session):
        return self.select_first({"email": email}, db)
    
    def create_user(self, user: CreateUserSchema, db: Session) -> CreateUserSchema:
        hashedPassword = get_password_hash(user.password)
        user.password = hashedPassword
        return self.insert(user, db)
    
user_repository = UserRepository()