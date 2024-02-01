from fastapi import FastAPI
from auth.router import auth_router
from user.router import user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)