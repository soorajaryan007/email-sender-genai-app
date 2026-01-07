from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    groq_api_key: str = Field(alias="GROQ_API_KEY")

    groq_model: str =  "llama-3.3-70b-versatile"
    groq_temperature: float = 0.4
    groq_max_tokens: int = 1024
    app_env: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        populate_by_name=True,
        extra="ignore",
    )


settings = Settings()
