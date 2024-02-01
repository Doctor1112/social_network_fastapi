from sqlalchemy import Boolean, Column, Integer, String
from db.init_db import Base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import uuid

class User(Base):

    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]