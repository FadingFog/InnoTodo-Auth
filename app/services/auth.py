from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_session
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.auth import TokenObtain, TokenPrivate
from app.services.base import BaseServices
from app.utils import password_helper, token_helper


class AuthServices(BaseServices):
    repository = UserRepository
    model = User

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)

    async def authenticate(self, input_schema: TokenObtain) -> tuple[User, str]:
        user = await self._repository.get_one_by_field("email", input_schema.email)
        await self._check_obj_404(user)

        verified = password_helper.verify_password(input_schema.password, user.hashed_password)

        if not verified:
            raise HTTPException(status_code=400)

        token_data = {'user_id': user.id}
        access_token = token_helper.create_access_token(token_data)

        return user, access_token

    async def create_private_token(self, input_schema: TokenPrivate) -> str:
        private_token = token_helper.create_private_token(input_schema.dict())
        return f'{settings.TOKEN_TYPE} {private_token}'
