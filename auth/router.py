from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.schemas import Token
from .service import AuthService
from user.schemas import UserCreate

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
          auth_service: AuthService = Depends()):
    token: str = await auth_service.login(form_data.username, form_data.password)

    return {"access_token": token, "token_type": "bearer"}
    
