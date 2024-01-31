from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user
from user.models import User

from .service import UserService
from user.schemas import UserCreate, UserOut

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/signup", response_model=UserOut, status_code=201)
async def signup(user: UserCreate,
                 user_service: UserService = Depends()):
    user = await user_service.signup(user)
    return user

@user_router.get("/me", response_model=UserOut)
def home(user: User = Depends(get_current_user)):
    return user
    
