from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    TARGET_URL: str = "http://localhost:3000"
    ADMIN_EMAIL: str = "admin@juice-sh.op"
    PROXY_URL: str | None = None
    
    # Path to the Juice Shop source code (required for coding challenges)
    JUICE_SHOP_SOURCE_PATH: Path = Path(__file__).resolve().parent.parent / "juice-shop-master"

    class Config:
        env_file = ".env"

settings = Settings()
