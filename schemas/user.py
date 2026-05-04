from pydantic import BaseModel, EmailStr


# Для регистрации и логина
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Ответ (необязательно, но правильно)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True