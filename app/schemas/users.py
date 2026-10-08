from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def password_must_contain_uppercase(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[\W_]', value):
            raise ValueError('Password must contain at least one special character')
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str