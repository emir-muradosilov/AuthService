
from pydantic import BaseModel, EmailStr, model_validator
from datetime import datetime
from app.models.models import Role


class UserCreate(BaseModel):
    user_name : str
    second_name : str | None = None
    patronymic : str | None = None
    email : EmailStr
    password : str
    password_confirm: str

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self


class UserLogin(BaseModel):
    email : EmailStr
    password : str


class UserDelete(BaseModel):
    id : int


class UserUpdate(BaseModel):
    user_name: str | None = None
    second_name: str | None = None
    patronymic: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: int
    user_name: str
    second_name: str
    patronymic: str
    email: str
    is_active :bool
    created_at : datetime
    updated_at : datetime
    role : str
