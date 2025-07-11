from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    cache_expire_http_responce: int

    class Config:
        env_file = ".env"

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"


settings = Settings()
