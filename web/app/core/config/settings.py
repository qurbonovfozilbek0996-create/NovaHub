from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "NovaHub"
    DEBUG: bool = False

    SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY"

    BOT_TOKEN: str

    WEB_APP_URL: str = "https://example.com"

    FOUNDER_TELEGRAM_ID: int = 8211219159

    DATABASE_URL: str = (
        "sqlite+aiosqlite:///./novahub.db"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
