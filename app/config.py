from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db_auth:5432/postgres"
    PRIVATE_SECRET_KEY: str = 'Hdpl8E4HNSYjI4YcLF2TjqgEMFaeghratyEe6lbVRVs='
    TOKEN_TYPE: str = 'Bearer'

    class Config:
        env_file = ".env"


settings = Settings()
