from datetime import timedelta, timezone
from datetime import datetime
from user.repo import UserRep
from sqlalchemy.ext.asyncio import AsyncSession
from db.init_db import get_db
from user.models import User
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from user.schemas import UserCreate
from core.config import cfg
from core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, rep: UserRep = Depends()):
        self._rep: UserRep = rep

    async def login(self, username: str, password: str):
        user: User = await self._rep.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return access_token
