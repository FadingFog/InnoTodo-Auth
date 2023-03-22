from fastapi import APIRouter, Depends

from app.dependecies.auth import get_current_user
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserChangePassword
from app.services.user import UserServices

router = APIRouter(dependencies=[Depends(get_current_user)], tags=['Users'])
router_registration = APIRouter(tags=['Users'])


@router_registration.post("/users", response_model=UserOut)
async def create_user(input_schema: UserCreate, service: UserServices = Depends(UserServices)):
    user = await service.create(input_schema)

    return user


@router.get("/users/{pk}", response_model=UserOut)
async def retrieve_user(pk: int, service: UserServices = Depends(UserServices)):
    users = await service.retrieve(pk)

    return users


@router.get("/users", response_model=list[UserOut])
async def get_all_users(service: UserServices = Depends(UserServices)):
    users = await service.get_all()

    return users


@router.patch("/users/{pk}", status_code=204)
async def update_user(pk: int, input_schema: UserUpdate, service: UserServices = Depends(UserServices)):
    result = await service.update(pk, input_schema)


@router.delete("/users/{pk}", status_code=204)
async def delete_user(pk: int, service: UserServices = Depends(UserServices)):
    result = await service.delete(pk)


@router.post("/users/{pk}/change_password", status_code=204)
async def change_password(pk: int, input_schema: UserChangePassword, service: UserServices = Depends(UserServices)):
    result = await service.change_password(pk, input_schema)
