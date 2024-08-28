import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class AGMSettings(BaseSettings):
    
    SQLITE3_FILE: str = os.getenv("SQLITE3_FILE", "roads.sqlite")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="UTF-8"
    )