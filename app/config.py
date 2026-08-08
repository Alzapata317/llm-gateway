from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    openai_api_key: SecretStr
    openai_base_url: str = "https://api.openai.com/v1"
    request_timeout_s: float = 30.0


settings = Settings()
