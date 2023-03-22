from typing import Protocol, Any


class RepositoryInterface(Protocol):
    async def get_by_id(self, obj_id: int):
        ...

    async def get_one_by_field(self, field: str, value: Any):
        ...

    async def get_all_by_field(self, field: str, value: Any):
        ...

    async def get_all(self):
        ...

    async def create(self, obj):
        ...

    async def update(self, obj_id: int, values: dict):
        ...

    async def delete(self, obj_id: int):
        ...
