import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

def require_environment_variable(name: str) -> str:
    """Return a required environment variable or raise a clear error."""

    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable {name!r} is missing."
        )

    return value

def optional_integer(name: str) -> int | None:
    """Read an optional integer environment variable."""

    value = os.getenv(name)

    if not value:
        return None

    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(
            f"Environment variable {name!r} must be an integer."
        ) from exc

@dataclass(frozen=True)
class Settings:
    discord_token: str
    guild_id: int | None
    log_level: str
    timezone: str


settings = Settings(
    discord_token=require_environment_variable("DISCORD_TOKEN"),
    guild_id=optional_integer("GUILD_ID"),
    log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    timezone=os.getenv("TIMEZONE", "Europe/London")
)

@dataclass(frozen=True)
class DatabaseConfig:
    database_path: Path = Path("data/dart_vader.db")