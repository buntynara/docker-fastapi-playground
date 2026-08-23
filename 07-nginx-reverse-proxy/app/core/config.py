from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Settings with default values
    APP_NAME: str = "Docker FastAPI Playground"
    APP_ENV: str = "development"

    MYSQL_HOST: str = "mysql"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "tasksdb"
    MYSQL_USER: str = "appuser"
    MYSQL_PASSWORD: str = ""
    MYSQL_ROOT_PASSWORD: str = ""

    # Pydantic Settings Configuration (overrides default behavior)
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

@lru_cache
def get_settings(): 
    return Settings()
