from fastapi import FastAPI

from app.api.routes import routes
from app.db import engine
from app.models.base import Base

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(routes, prefix='/api')
