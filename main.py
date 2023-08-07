from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import routes
from app.db import engine
from app.models.base import Base

app = FastAPI()

origins = [
    "http://localhost:5173",
]

headers = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=headers,
    expose_headers=["*"],
)


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(routes, prefix='/api')
