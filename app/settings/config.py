from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    environment: str = Field(alias="ENVIRONMENT", default="local")
    redis_host: str = Field(alias="REDIS_HOST", default="redis")
    redis_db: int = Field(alias="REDIS_DB", default=0)
    redis_port: int = Field(alias="REDIS_PORT", default=6379)
