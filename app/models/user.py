from sqlalchemy import Boolean, Column, String

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
