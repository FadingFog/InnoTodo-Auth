from abc import abstractproperty
from typing import TypeVar, Any, Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository import RepositoryInterface
from app.models import Base

PydanticModel = TypeVar('PydanticModel', bound=BaseModel)
Model = TypeVar('Model', bound=Base)
Repository = TypeVar('Repository', bound=RepositoryInterface)


class BaseServices:
    repository: Repository = abstractproperty
    model: Type[Model] = abstractproperty

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = self.repository(self.session)

    async def _check_obj_404(self, obj: Any):
        if obj is None:
            raise HTTPException(status_code=404)

    async def create(self, input_schema: PydanticModel) -> Model:
        obj = self.model(**input_schema.dict())
        obj = await self._repository.create(obj)

        return obj

    async def retrieve(self, obj_id: int) -> Model:
        obj = await self._repository.get_by_id(obj_id)
        await self._check_obj_404(obj)

        return obj

    async def update(self, obj_id: int, input_schema: PydanticModel) -> Result:
        values = input_schema.dict(exclude_unset=True)
        result = await self._repository.update(obj_id, values)

        if result.rowcount < 1:
            raise HTTPException(status_code=404)

        return result

    async def delete(self, obj_id: int) -> Result:
        result = await self._repository.delete(obj_id)

        if result.rowcount < 1:
            raise HTTPException(status_code=404)

        return result
