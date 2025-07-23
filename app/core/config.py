from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    frontend_url: str
    default_ratelimit_num: int
    default_ratelimit_time: int
    secret_key: str
    jwt_algorithm: str
    access_token_expires: int
    refresh_token_expires: int
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    redis_url: str
    cache_expire_http_responce: int
    email_user: str
    email_password: str

    class Config:
        env_file = ".env"

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"


settings = Settings()
