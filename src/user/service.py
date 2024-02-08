import uuid
from fastapi import Depends, HTTPException, status

from user.models import FriendRequest
from .repo import UserRep, FriendRequestRep
from .schemas import UserCreate, UserInDb
from core.security import get_password_hash
from core.exceptions import UserNotFoundException, FriendRequestNotFoundException


class UserService:
    def __init__(self, user_rep: UserRep = Depends(),
                 friend_request_rep: FriendRequestRep = Depends()):
        self._user_rep: UserRep = user_rep
        self._friend_req_rep: FriendRequestRep = friend_request_rep

    async def signup(self, user_data: UserCreate):
        user = await self._user_rep.get_by_username(user_data.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="a user with this username already exists",
            )
        if user_data.email:
            user = await self._user_rep.get_by_email(user_data.email)
            if user:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="a user with this email already exists",
            )
        hashed_password = get_password_hash(user_data.password)
        user_db = UserInDb(**user_data.model_dump(), hashed_password=hashed_password)

        user = await self._user_rep.create(user_db)
        return user
    
    async def are_friends(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID) -> bool:
        friendship = await self._user_rep.get_friendship(user_id_1, user_id_2)
        return not (friendship is None)
    
    async def send_friend_request(self, sender_id, receiver_id) -> FriendRequest:
        are_friends = await self.are_friends(sender_id, receiver_id)
        if are_friends:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="these users are already friends")
        req = await self._friend_req_rep.get_by_id(sender_id, receiver_id)
        if req:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="this friend request already exists")
        receiver = await self._user_rep.get_by_id(receiver_id)
        if receiver is None:
            raise UserNotFoundException(receiver_id)
        sender = await self._user_rep.get_by_id(sender_id)
        if sender is None:
            raise UserNotFoundException(sender_id)
        request = await self._friend_req_rep.create(sender_id=sender_id, receiver_id=receiver_id)
        return request
    
    async def accept_friend_request(self, sender_id, receiver_id):
        request = await self._friend_req_rep.get_by_id(sender_id=sender_id, receiver_id=receiver_id)
        if request is None:
            raise FriendRequestNotFoundException(sender_id=sender_id,
                                                 receiver_id=receiver_id)
        sender = await self._user_rep.get_by_id(sender_id)
        if sender is None:
            raise UserNotFoundException(sender_id)
        receiver = await self._user_rep.get_by_id(receiver_id)
        if receiver is None:
            raise UserNotFoundException(receiver_id)
        await self._user_rep.add_friend(sender, receiver)
        await self._friend_req_rep.delete(request)

    async def delete_friend_request(self, sender_id, receiver_id):
        request = await self._friend_req_rep.get_by_id(sender_id=sender_id, receiver_id=receiver_id)
        if request is None:
            raise FriendRequestNotFoundException(sender_id=sender_id,
                                                 receiver_id=receiver_id)
        await self._friend_req_rep.delete(request)

        