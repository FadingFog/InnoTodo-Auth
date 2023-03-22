from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=True)


async def get_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as exc:
            logger.error(exc)
            await session.rollback()
