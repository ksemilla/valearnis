from ninja import Schema
from pydantic import EmailStr, validator
from .models import User


class CreateUserSchema(Schema):
    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, value):
        if User.objects.filter(email=value).exists():
            raise ValueError("email already in use")
        return value


class UserSchema(Schema):
    id: int
    email: EmailStr
    name: str
    role: str


class UserUpdateSchema(Schema):
    name: str = None
    role: str = "user"


class StatsSchema(Schema):
    total_quizzes: int
    average_percentage: float
