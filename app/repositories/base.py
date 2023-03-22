from abc import abstractproperty
from typing import TypeVar, Type, Any, Generic

from sqlalchemy import select, delete, update, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository import RepositoryInterface
from app.models.base import Base

Model = TypeVar('Model', bound=Base)


class BaseRepository(RepositoryInterface, Generic[Model]):
    model: Type[Model] = abstractproperty

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, obj_id: int) -> Model | None:
        result = await self.session.scalars(
            select(self.model).where(getattr(self.model, 'id') == obj_id))
        obj = result.one_or_none()
        return obj

    async def get_one_by_field(self, field: str, value: Any) -> Model | None:
        result = await self.session.scalars(select(self.model).where(getattr(self.model, field) == value))
        obj = result.one_or_none()
        return obj

    async def get_all_by_field(self, field: str, value: Any) -> list[Model | None]:
        result = await self.session.scalars(select(self.model).where(getattr(self.model, field) == value))
        objects = result.all()
        return objects

    async def get_all(self) -> list[Model | None]:
        result = await self.session.scalars(select(self.model))
        objects = result.all()
        return objects

    async def create(self, obj: Model) -> Model:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def update(self, obj_id: int, values: dict) -> Result:
        result = await self.session.execute(update(self.model).where(self.model.id == obj_id).values(**values))

        if result.rowcount > 0:
            await self.session.flush()

        return result

    async def delete(self, obj_id: int) -> Result:
        result = await self.session.execute(delete(self.model).where(self.model.id == obj_id))

        if result.rowcount > 0:
            await self.session.flush()

        return result
