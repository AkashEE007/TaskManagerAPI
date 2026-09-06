from pydantic_settings import BaseSettings, SettingsConfigDict
# from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_CONNECTION:str | None = None
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int


settings = Settings()


# print(settings.DB_CONNECTION)