from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from core.config import cfg

engine = create_async_engine(cfg.SQLALCHEMY_DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()