import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from db.init_db import Base, get_db
from src.main import app
from auth.schemas import Token

# DATABASE
DATABASE_URL_TEST = "sqlite+aiosqlite:///test.db"

BASE_URL = "http://test"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.engine = engine_test

async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = async_session


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def logged_in_client() -> AsyncGenerator[AsyncClient, None]:
    
    username = "user"
    password = "password"
    first_name = "fname"
    last_name = "lname"

    async with AsyncClient(app=app,
                           base_url=BASE_URL) as conn:
        register_response = await conn.post("/users/signup", json=dict(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name))
        token_response = await conn.post("/auth/token", data=dict(
            username=username,
            password=password))
        token = Token(**token_response.json())
        headers = {"Authorization": f"Bearer "
                                f"{token.access_token}"}

    async with AsyncClient(app=app,
                           base_url=BASE_URL,
                           headers=headers) as new_user_conn:
        yield new_user_conn

# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        yield ac

