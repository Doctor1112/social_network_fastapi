from typing import AsyncGenerator
from httpx import AsyncClient
import pytest
from main import app
from auth.schemas import Token
from core.security import get_password_hash
from tests.conftest import async_session
from user.models import User
from user.repo import UserRep
from user.schemas import UserInDb
from sqlalchemy.ext.asyncio import AsyncSession
from user.service import UserService, FriendRequestRep
import faker
from user.models import User

@pytest.fixture()
async def user_rep(async_session: AsyncSession):
    return UserRep(async_session)

@pytest.fixture()
async def friend_request_rep(async_session: AsyncSession):
    return FriendRequestRep(async_session)


@pytest.fixture()
async def user_service(user_rep: UserRep, friend_request_rep: FriendRequestRep):
    return UserService(user_rep=user_rep, friend_request_rep=friend_request_rep)


@pytest.fixture()
async def friend_req_rep(async_session: AsyncSession):
    return FriendRequestRep(async_session)

@pytest.fixture()
async def user_factory(async_session: AsyncSession):
    fake = faker.Faker()
    async def inner():
        user = User(username=fake.unique.user_name(),
                    first_name=fake.unique.first_name(),
                    last_name=fake.unique.last_name(),
                    hashed_password=fake.password(),
                    email=fake.unique.email())
        async_session.add(user)
        await async_session.commit()
        return user
    return inner