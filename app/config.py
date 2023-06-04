# in this file we are going to define a pydantic model to validate our environment variables:
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_name: str
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int

    class Config:
        env_file = ".env"


setting = Settings()
