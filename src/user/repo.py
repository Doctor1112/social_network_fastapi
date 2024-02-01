from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from db.init_db import get_db
from .schemas import UserInDb

class UserRep:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        
    async def get_by_id(self):
        return await self.db.get(User, id)
    
    async def get_by_username(self, username: str):
        query = select(User).where(User.username == username)
        res = await self.db.execute(query)
        return res.scalar_one_or_none()
    
    async def get_by_email(self, email: str):
        query = select(User).where(User.email == email)
        res = await self.db.execute(query)
        return res.scalar_one_or_none()
    
    async def create(self, user: UserInDb):
        user = User(**user.model_dump())
        self.db.add(user)
        await self.db.commit()
        return user
    