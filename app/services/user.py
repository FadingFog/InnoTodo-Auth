from fastapi import Depends, HTTPException
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.base import BaseServices, PydanticModel
from app.utils import password_helper


class UserServices(BaseServices):
    repository = UserRepository
    model = User

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)

    async def get_all(self) -> list[User | None]:
        users = await self._repository.get_all()
        return users

    async def create(self, input_schema: UserCreate) -> User:
        hashed_password = password_helper.get_hash_password(input_schema.password)
        user = User(email=input_schema.email, hashed_password=hashed_password)
        exists = await self._repository.get_one_by_field('email', user.email)

        if exists:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        user = await self._repository.create(user)
        return user

    async def change_password(self, user_id: int, input_schema: PydanticModel) -> Result:
        new_password = password_helper.get_hash_password(input_schema.password)
        values = {'hashed_password': new_password}

        result = await self._repository.update(user_id, values)
        return result
