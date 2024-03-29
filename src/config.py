from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Settings class for bot.
    """

    bot_token: str = Field()
    database_url: str = Field()


settings = Settings()
