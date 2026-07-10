from pathlib import Path
import aiosqlite
from config.settings import DatabaseConfig

class DatabaseService:
    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config
        self.connection: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        database_path: Path = self._config.database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = await aiosqlite.connect(database_path)
        self.connection.row_factory = aiosqlite.Row
        await self.connection.execute('PRAGMA foreign_keys = ON')
        await self.connection.commit()

    async def initialise(self) -> None:
        if self.connection is None:
            raise RuntimeError('Database connection has not been opened.')
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                display_name TEXT NOT NULL,
                joined_at TEXT NOT NULL,
                UNIQUE(discord_user_id, guild_id)
            )
        """)
        await self.connection.commit()

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()