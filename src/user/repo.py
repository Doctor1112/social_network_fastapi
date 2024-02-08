import uuid
from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, FriendRequest, friends_table
from db.init_db import get_db
from .schemas import UserInDb
from sqlalchemy import func
from sqlalchemy.orm import selectinload

class UserRep:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self._db = db
        
    async def get_by_id(self, id: uuid.UUID) -> User | None:
        return await self._db.get(User, id)
    
    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        res = await self._db.execute(query)
        return res.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        res = await self._db.execute(query)
        return res.scalar_one_or_none()
    
    async def get_friends(self, user: User):
        query = select(User).where(User.id == user.id).options(
            selectinload(User.friends))
        res = await self._db.execute(query)
        return res.scalar().friends
    
    async def get_friendship(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID):
        query = select(friends_table).where(
            friends_table.c.user_left_id == user_id_1,
            friends_table.c.user_right_id == user_id_2
            )
        res = await self._db.execute(query)
        return res.scalar_one_or_none()
        
    
    async def create(self, user: UserInDb) -> User:
        user = User(**user.model_dump())
        self._db.add(user)
        await self._db.commit()
        return user
    
    async def add_friend(self, user_1: User, user_2: User):
        user_friends_1 = await self.get_friends(user_1)
        user_friends_2 = await self.get_friends(user_2)
        user_friends_1.add(user_2)
        user_friends_2.add(user_1)
        await self._db.commit()

class FriendRequestRep:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self._db = db

    async def create(self, sender_id: uuid.UUID, receiver_id: uuid.UUID) -> FriendRequest:
        friend_request = FriendRequest(sender_id=sender_id, receiver_id=receiver_id)
        self._db.add(friend_request)
        await self._db.commit()
        return friend_request
    
    async def delete(self, request: FriendRequest):
        await self._db.delete(request)
        await self._db.commit()

    async def get_by_id(self, sender_id: uuid.UUID, receiver_id: uuid.UUID):
        query = select(FriendRequest).where(FriendRequest.sender_id==sender_id,
                                          FriendRequest.receiver_id==receiver_id)
        res = await self._db.execute(query)
        return res.scalar_one_or_none()
    
    async def count(self) -> int | None:
        query = await self._db.execute(func.count(FriendRequest.sender_id))
        return query.scalar()
        


    

    