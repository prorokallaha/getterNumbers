import os
from pathlib import Path
from typing import (
    List,
    Optional,
    TypeAlias,
    Union,
)

from aiogram.enums.parse_mode import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict

_StrPath: TypeAlias = Union[os.PathLike[str], str, Path]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="DATABASE_",
    )

    uri: str
    name: str
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    echo: Optional[bool] = None
    future: Optional[bool] = True

    @property
    def url(self) -> str:
        if "sqlite" in self.uri:
            return self.uri.format(self.name)
        return self.uri.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name,
        )


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="BOT_",
    )

    token: str
    admins: List[int] = []
    parse_mode: Union[ParseMode, str] = ParseMode.HTML
    disable_web_page_preview: Optional[bool] = True
    protect_content: Optional[bool] = None


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="REDIS_",
    )
    host: str = "127.0.0.1"
    port: int = 6379


class Settings(BaseSettings):
    bot: BotSettings
    redis: RedisSettings
    db: DatabaseSettings

    @staticmethod
    def root_dir() -> Path:
        return Path(__file__).resolve().parent.parent.parent

    @classmethod
    def path(cls, *paths: _StrPath, base_path: Optional[_StrPath] = None) -> str:
        if base_path is None:
            base_path = cls.root_dir()

        return os.path.join(base_path, *paths)


def load_settings(
    bot_settings: Optional[BotSettings] = None,
    redis_settings: Optional[RedisSettings] = None,
    database_settings: Optional[DatabaseSettings] = None,
) -> Settings:
    return Settings(
        bot=bot_settings or BotSettings(),  # type: ignore
        redis=redis_settings or RedisSettings(),
        db=database_settings or DatabaseSettings(),  # type: ignore
    )
