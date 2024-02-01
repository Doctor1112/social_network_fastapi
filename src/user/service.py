from fastapi import Depends, HTTPException, status
from .repo import UserRep
from .schemas import UserCreate, UserInDb
from core.security import get_password_hash


class UserService:
    def __init__(self, rep: UserRep = Depends()):
        self._rep: UserRep = rep

    async def signup(self, user_data: UserCreate):
        user = await self._rep.get_by_username(user_data.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="a user with this username already exists",
            )
        if user_data.email:
            user = await self._rep.get_by_email(user_data.email)
            if user:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="a user with this email already exists",
            )
        hashed_password = get_password_hash(user_data.password)
        user_db = UserInDb(**user_data.model_dump(), hashed_password=hashed_password)

        user = await self._rep.create(user_db)
        return user
