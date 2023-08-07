from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User
from app.repositories.user import UserRepository
from app.utils import token_helper

auth_scheme = HTTPBearer()


async def get_current_user(
        access_token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        session: AsyncSession = Depends(get_session)
) -> User:
    repository = UserRepository(session)
    token = access_token.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authentication": "Bearer"},
    )

    try:
        payload = token_helper.get_token_payload(token)
        user_id: int = payload.get("user_id")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await repository.get_by_id(user_id)
    if not user:
        raise credentials_exception

    return user
