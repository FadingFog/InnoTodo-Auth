from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_id_with_lists(self, user_id: int):
        result = await self.session.scalars(
            select(self.model).where(self.model.id == user_id).options(joinedload(self.model.lists))
        )
        user = result.unique().first()
        return user
