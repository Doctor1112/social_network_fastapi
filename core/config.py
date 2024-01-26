from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///database.db"
    JWT_SECRET_KEY: str = "607a516c4bf407db540d027bac92d7f28344588e675fcf3852022c07dc8c59c6"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"


cfg = Settings()