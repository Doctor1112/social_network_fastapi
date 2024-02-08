from typing import Coroutine
from fastapi import HTTPException, Response
from tests.conftest import client
from httpx import Response
from httpx import AsyncClient
from user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from user.service import UserService
from user.repo import FriendRequestRep, UserRep
import uuid
import pytest
from core.exceptions import UserNotFoundException, FriendRequestNotFoundException


async def test_send_request(user_factory,
                            user_service: UserService,
                            friend_req_rep: FriendRequestRep):
    t = type(user_factory)
    sender = await user_factory()
    receiver = await user_factory()
    req = await user_service.send_friend_request(sender.id, receiver.id)
    req = await friend_req_rep.get_by_id(sender_id=sender.id,
                                                     receiver_id=receiver.id)
    assert req
    assert req.sender_id == sender.id
    assert req.receiver_id == receiver.id

async def test_send_request_to_unexisting_user(user_factory,
                                               user_service: UserService):
    sender = await user_factory()
    receiver_id = uuid.uuid1()
    with pytest.raises(UserNotFoundException):
        await user_service.send_friend_request(sender_id=sender.id,
                                            receiver_id=receiver_id)


async def test_add_friend(user_factory,
                          user_service: UserService,
                          user_rep: UserRep):
    user_1 = await user_factory()
    user_2 = await user_factory()
    is_friend = await user_service.are_friends(user_1.id, user_2.id)
    assert not is_friend
    await user_rep.add_friend(user_1, user_2)
    are_friends = await user_service.are_friends(user_1.id, user_2.id)
    assert are_friends


async def test_accept_request(user_factory,
                              user_service: UserService,
                              friend_req_rep: FriendRequestRep):
    user_1 = await user_factory()
    user_2 = await user_factory()
    req = await user_service.send_friend_request(user_1.id, user_2.id)
    await user_service.accept_friend_request(req.sender_id, req.receiver_id)
    are_friends = await user_service.are_friends(user_1.id, user_2.id)
    assert are_friends

async def test_accept_unexisting_request(user_factory,
                                         user_service: UserService):
    receiver = await user_factory()
    sender = await user_factory()
    with pytest.raises(FriendRequestNotFoundException):
        await user_service.accept_friend_request(receiver_id=receiver.id,
                                                 sender_id=sender.id)
        
async def test_delete_unexisting_request(user_service: UserService):
    sender_id = uuid.uuid1()
    receiver_id = uuid.uuid1()
    with pytest.raises(FriendRequestNotFoundException):
        await user_service.delete_friend_request(sender_id=sender_id,
                                                receiver_id=receiver_id)
        
async def test_delete_friend_request(user_service: UserService,
                                     user_factory,
                                     friend_req_rep: FriendRequestRep):
    sender = await user_factory()
    receiver = await user_factory()
    await user_service.send_friend_request(sender_id=sender.id,
                                           receiver_id=receiver.id)
    await user_service.delete_friend_request(sender_id=sender.id,
                                                   receiver_id=receiver.id)
    req = await friend_req_rep.get_by_id(sender_id=sender.id, receiver_id=receiver.id)
    assert req is None


async def test_send_existing_friend_request(user_service: UserService,
                                            user_factory):
    sender = await user_factory()
    receiver = await user_factory()
    req = await user_service.send_friend_request(sender_id=sender.id,
                                           receiver_id=receiver.id)
    with pytest.raises(HTTPException):
        req = await user_service.send_friend_request(sender_id=sender.id,
                                            receiver_id=receiver.id)
    
    
    

        




