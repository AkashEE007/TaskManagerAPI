from pydantic_settings import BaseSettings, SettingsConfigDict
# from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_CONNECTION:str | None = None


settings = Settings()


# print(settings.DB_CONNECTION)