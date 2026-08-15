from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "NovaHub"
    DEBUG: bool = False

    SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY"

    BOT_TOKEN: str

    WEB_APP_URL: str = ""

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "NovaHub"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    FOUNDER_TELEGRAM_ID: int = 8211219159

    DATABASE_URL: str = "sqlite+aiosqlite:///./novahub.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
