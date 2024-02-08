from sqlalchemy import Boolean, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Table
from db.init_db import Base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Set
import uuid


friends_table = Table(
    "friends",
    Base.metadata,
    Column("user_left_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("user_right_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):

    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    friends: Mapped[Set["User"]] = relationship(secondary=friends_table, 
                                                primaryjoin = (friends_table.c.user_left_id == id),
                                                secondaryjoin = (friends_table.c.user_right_id == id),
                                                lazy='selectin')

class FriendRequest(Base):

    __tablename__ = "friend_request"

    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    receiver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    sender: Mapped[User] = relationship(backref="sended_requests", foreign_keys=[sender_id])
    receiver: Mapped[User] = relationship(backref="received_requests", foreign_keys=[receiver_id])
