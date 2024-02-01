from uuid import UUID
from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):

    username: str
    first_name: str
    last_name: str
    email: EmailStr | None = None

class UserCreate(BaseUser):
    
    password: str

class UserInDb(BaseUser):

    hashed_password: str

class UserOut(BaseUser):
    id: UUID