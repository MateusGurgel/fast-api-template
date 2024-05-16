from sqlalchemy.orm import Session
from src.modules.user.user_schemas import CreateUserSchema
from src.modules.user.user import User
from src.utils.encryption import get_password_hash


def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


def get_user_by_(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def create_user(user: CreateUserSchema, db: Session) -> CreateUserSchema:
    hashedPassword = get_password_hash(user.password)
    db_user = User(**user.model_dump())
    db_user.password = hashedPassword
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
