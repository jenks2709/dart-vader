from datetime import datetime
import aiosqlite
from models.member import Member

class MemberRepository:
    def __init__(self, connection: aiosqlite.Connection) -> None:
        self._connection = connection

    async def create(
    self,
    discord_user_id: int,
    guild_id: int,
    first_name: str,
    last_name: str,
    display_name: str,
) -> Member:
        joined_at = datetime.now().astimezone()
        cursor = await self._connection.execute(
    """
    INSERT INTO members (
        discord_user_id,
        guild_id,
        first_name,
        last_name,
        display_name,
        joined_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        discord_user_id,
        guild_id,
        first_name,
        last_name,
        display_name,
        joined_at.isoformat(),
    ),
)
        await self._connection.commit()
        return Member(
            id=cursor.lastrowid,
            discord_user_id=discord_user_id,
            guild_id=guild_id,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            joined_at=joined_at,
        )

    async def get_by_discord_id(
        self,
        discord_user_id: int,
        guild_id: int,
    ) -> Member | None:
        cursor = await self._connection.execute(
            """
            SELECT
                id,
                discord_user_id,
                guild_id,
                first_name,
                last_name,
                display_name,
                joined_at
            FROM members
            WHERE discord_user_id = ?
            AND guild_id = ?
            """,
            (
                discord_user_id,
                guild_id,
            ),
        )

        row = await cursor.fetchone()

        if row is None:
            return None

        return Member(
            id=row["id"],
            discord_user_id=row["discord_user_id"],
            guild_id=row["guild_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            display_name=row["display_name"],
            joined_at=datetime.fromisoformat(
                row["joined_at"]
            ),
        )
    async def list_by_guild(
        self,
        *,
        guild_id: int,
    ) -> list[Member]:
        cursor = await self._connection.execute(
            """
            SELECT
                id,
                discord_user_id,
                guild_id,
                first_name,
                last_name,
                display_name,
                joined_at
            FROM members
            WHERE guild_id = ?
            ORDER BY
                last_name COLLATE NOCASE ASC,
                first_name COLLATE NOCASE ASC
            """,
            (guild_id,),
        )

        rows = await cursor.fetchall()

        return [
            Member(
                id=row["id"],
                discord_user_id=row["discord_user_id"],
                guild_id=row["guild_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                display_name=row["display_name"],
                joined_at=datetime.fromisoformat(row["joined_at"]),
            )
            for row in rows
        ]