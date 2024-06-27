from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserListSchema(BaseModel):
    username: str
    email: EmailStr
