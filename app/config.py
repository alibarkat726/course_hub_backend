import os
from functools import lru_cache
from dotenv import load_dotenv
# 👇 Load environment variables from the .env file
load_dotenv()


class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:user@localhost:5432/coursehub",
    )

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "43200"))  # 30 days
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # Multi-tenancy
    TENANT_HEADER: str = os.getenv("TENANT_HEADER", "X-Tenant-ID")

    # Stripe
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")


@lru_cache()
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()
