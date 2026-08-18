from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )
    
    database_url: str
    port: int = 8000
    pokeapi_url: str
    
    postgres_user: str
    postgres_password: str
    postgres_db: str
    test_database_url: str | None = None
    test_postgres_db: str | None = None

settings = Settings()