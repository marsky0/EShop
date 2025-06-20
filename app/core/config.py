from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    cache_expire_http_responce: int

    class Config:
        env_file = ".env"

settings = Settings()
