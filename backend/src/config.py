"""Global application configuration."""
import os

DB_URL = "sqlite:///data.db"

DB_CONNECTION_ARGS = {
    "check_same_thread": False,
}

REDIS_HOST = os.getenv("REDIS_HOST") or "127.0.0.1"
REDIS_PORT = os.getenv("REDIS_PORT") or "6379"
REDIS_APP_PREFIX = "slides"
