# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import field_validator

# class Settings(BaseSettings):
#     database_url: str = "sqlite:///./devtrack.db"

#     @field_validator("database_url", mode="before")
#     @classmethod
#     def assemble_db_connection(cls, v: str) -> str:
#         if isinstance(v, str) and v.startswith("postgres://"):
#             return v.replace("postgres://", "postgresql://", 1)
#         return v
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int

#     model_config = SettingsConfigDict(env_file=".env")

# settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    database_url: str = "sqlite:///./devtrack.db"
    secret_key: str = "devtrack_secret_key_123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @field_validator("database_url", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()