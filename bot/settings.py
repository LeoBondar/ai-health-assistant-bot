import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis

class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

class BotSettings(CustomBaseSettings):
    token: str
    album_timeout: int = 5
    parse_mode: Literal["MARKDOWN_V2", "MARKDOWN", "HTML"] = "HTML"
    drop_pending_updates: bool = True
    rate_limit: int | float = 1

class LoggingSettings(CustomBaseSettings):
    level: int = 10

class RedisSettings(CustomBaseSettings):
    use: bool
    host: str
    port: int
    expose_port: int
    password: str

    def get_redis(self, db: int = 0) -> Redis:
        return Redis(host=self.host, port=self.port, password=self.password, db=db)

class AIHealthAssistantSettings(BaseSettings):
    base_url: str
    connect_timeout: float
    connection_limit: int
    validate_cert: bool
    total_timeout: float

class Settings(CustomBaseSettings):
    load_dotenv()
    bot: BotSettings = BotSettings(_env_prefix="BOT_")
    logging: LoggingSettings = LoggingSettings(_env_prefix="LOG_")
    redis: RedisSettings = RedisSettings(_env_prefix="REDIS_")
    ai: AIHealthAssistantSettings = AIHealthAssistantSettings(_env_prefix="AI_")

def load_settings() -> Settings:
    return Settings()

settings = load_settings()
