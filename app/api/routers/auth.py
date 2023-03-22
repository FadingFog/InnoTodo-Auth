from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger

from app.dependecies.auth import get_current_user
from app.models import User
from app.schemas.auth import TokenObtain, TokenPrivate
from app.services.auth import AuthServices

router = APIRouter(tags=['Auth'])


@router.get("/auth", status_code=200)
async def authorize_user(user: User = Depends(get_current_user), service: AuthServices = Depends(AuthServices)):
    logger.debug(f'User {user.id} authorized')

    private_token_data = TokenPrivate(user_id=user.id)
    private_token = await service.create_private_token(private_token_data)

    return JSONResponse({'status': 'success'}, headers={'Authorization': private_token})


@router.post("/auth", status_code=200)
async def obtain_token(input_schema: TokenObtain, service: AuthServices = Depends(AuthServices)):
    user, access_token = await service.authenticate(input_schema)

    data = {'access_token': access_token, 'token_type': 'bearer'}
    return JSONResponse(content=data)
