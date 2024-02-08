import uuid
from fastapi import APIRouter, Depends, status

from auth.dependencies import get_current_user
from user.models import User

from .service import UserService
from user.schemas import FriendRequestSchema, UserCreate, UserOut

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/signup", response_model=UserOut, status_code=201)
async def signup(user: UserCreate,
                 user_service: UserService = Depends()):
    user = await user_service.signup(user)
    return user

@user_router.get("/me", response_model=UserOut)
def home(cur_user: User = Depends(get_current_user)):
    return cur_user

@user_router.post("/send_friend_request/{receiver_id}", response_model=FriendRequestSchema)
async def send_friend_request(receiver_id: uuid.UUID,
                              cur_user: User = Depends(get_current_user),
                              user_service: UserService = Depends()):
    friend_request = await user_service.send_friend_request(cur_user.id, receiver_id=receiver_id)
    return friend_request

@user_router.post("/accept_friend_request/{sender_id}")
async def accept_friend_request(sender_id: uuid.UUID,
                                cur_user: User = Depends(get_current_user),
                                user_service: UserService = Depends()):
    await user_service.accept_friend_request(sender_id=sender_id,
                                             receiver_id=cur_user.id)
    
@user_router.delete("/reject_friend_request/{sender_id}", status_code=status.HTTP_202_ACCEPTED)
async def reject_friend_request(sender_id: uuid.UUID,
                                cur_user: User = Depends(get_current_user),
                                user_service: UserService = Depends()):
    await user_service.delete_friend_request(sender_id=sender_id,
                                             receiver_id=cur_user.id)
    
@user_router.delete("/cancel_friend_request/{receiver_id}", status_code=status.HTTP_202_ACCEPTED)
async def cancel_friend_request(receiver_id: uuid.UUID,
                                cur_user: User = Depends(get_current_user),
                                user_service: UserService = Depends()):
    await user_service.delete_friend_request(sender_id=cur_user.id,
                                             receiver_id=receiver_id)
    
    
    
    
