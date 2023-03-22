from pydantic import BaseModel, EmailStr


class TokenObtain(BaseModel):
    email: EmailStr
    password: str


class TokenPrivate(BaseModel):
    user_id: int
