from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserListSchema(BaseModel):
    username: str
    email: EmailStr