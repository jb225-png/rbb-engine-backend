from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    environment: str
    database_url: str
    storage_path: str
    log_level: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
