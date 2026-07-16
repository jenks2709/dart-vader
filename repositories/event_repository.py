from datetime import datetime

from models.event import Event, EventStatus
from services.database_service import DatabaseService


class EventRepository:
    def __init__(self, database: DatabaseService) -> None:
        self.database = database

    async def create(
        self,
        *,
        guild_id: int,
        title: str,
        description: str,
        location: str,
        start_time: datetime,
        end_time: datetime | None,
        signup_deadline: datetime | None,
        maximum_attendees: int | None,
        status: EventStatus,
        created_by_discord_id: int,
    ) -> Event:
        created_at = datetime.now().astimezone()
        updated_at = created_at

        cursor = await self.database.execute(
            """
            INSERT INTO events (
                guild_id,
                title,
                description,
                location,
                start_time,
                end_time,
                signup_deadline,
                maximum_attendees,
                status,
                created_by_discord_id,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                guild_id,
                title,
                description,
                location,
                start_time.isoformat(),
                end_time.isoformat() if end_time else None,
                signup_deadline.isoformat() if signup_deadline else None,
                maximum_attendees,
                status.value,
                created_by_discord_id,
                created_at.isoformat(),
                updated_at.isoformat(),
            ),
        )

        await self.database.commit()

        return Event(
            id=cursor.lastrowid,
            guild_id=guild_id,
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            signup_deadline=signup_deadline,
            maximum_attendees=maximum_attendees,
            status=status,
            created_by_discord_id=created_by_discord_id,
            created_at=created_at,
            updated_at=updated_at,
        )
    async def list_upcoming(
        self,
        guild_id: int,
        limit: int = 10,
    ) -> list[Event]:
        cursor = await self.database.execute(
            """
            SELECT
                id,
                guild_id,
                title,
                description,
                location,
                start_time,
                end_time,
                signup_deadline,
                maximum_attendees,
                status,
                created_by_discord_id,
                created_at,
                updated_at
            FROM events
            WHERE guild_id = ?
            AND start_time > ?
            AND status = ?
            ORDER BY start_time ASC
            LIMIT ?
            """,
            (
                guild_id,
                datetime.now().astimezone().isoformat(),
                EventStatus.SCHEDULED.value,
                limit,
            ),
        )

        rows = await cursor.fetchall()

        return [
            Event(
                id=row["id"],
                guild_id=row["guild_id"],
                title=row["title"],
                description=row["description"],
                location=row["location"],
                start_time=datetime.fromisoformat(row["start_time"]),
                end_time=(
                    datetime.fromisoformat(row["end_time"])
                    if row["end_time"] is not None
                    else None
                ),
                signup_deadline=(
                    datetime.fromisoformat(row["signup_deadline"])
                    if row["signup_deadline"] is not None
                    else None
                ),
                maximum_attendees=row["maximum_attendees"],
                status=EventStatus(row["status"]),
                created_by_discord_id=row["created_by_discord_id"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )
            for row in rows
        ]
    async def get_by_id(
        self,
        *,
        guild_id: int,
        event_id: int,
    ) -> Event | None:
        cursor = await self.database.execute(
            """
            SELECT
                id,
                guild_id,
                title,
                description,
                location,
                start_time,
                end_time,
                signup_deadline,
                maximum_attendees,
                status,
                created_by_discord_id,
                created_at,
                updated_at
            FROM events
            WHERE guild_id = ?
            AND id = ?
            LIMIT 1
            """,
            (
                guild_id,
                event_id,
            ),
        )

        row = await cursor.fetchone()

        if row is None:
            return None

        return Event(
            id=row["id"],
            guild_id=row["guild_id"],
            title=row["title"],
            description=row["description"],
            location=row["location"],
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=(
                datetime.fromisoformat(row["end_time"])
                if row["end_time"] is not None
                else None
            ),
            signup_deadline=(
                datetime.fromisoformat(row["signup_deadline"])
                if row["signup_deadline"] is not None
                else None
            ),
            maximum_attendees=row["maximum_attendees"],
            status=EventStatus(row["status"]),
            created_by_discord_id=row["created_by_discord_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
    async def update(
        self,
        *,
        event: Event,
    ) -> Event:
        updated_at = datetime.now().astimezone()

        await self.database.execute(
            """
            UPDATE events
            SET
                title = ?,
                description = ?,
                location = ?,
                start_time = ?,
                end_time = ?,
                signup_deadline = ?,
                maximum_attendees = ?,
                status = ?,
                updated_at = ?
            WHERE guild_id = ?
            AND id = ?
            """,
            (
                event.title,
                event.description,
                event.location,
                event.start_time.isoformat(),
                (
                    event.end_time.isoformat()
                    if event.end_time is not None
                    else None
                ),
                (
                    event.signup_deadline.isoformat()
                    if event.signup_deadline is not None
                    else None
                ),
                event.maximum_attendees,
                event.status.value,
                updated_at.isoformat(),
                event.guild_id,
                event.id,
            ),
        )

        await self.database.commit()

        return Event(
            id=event.id,
            guild_id=event.guild_id,
            title=event.title,
            description=event.description,
            location=event.location,
            start_time=event.start_time,
            end_time=event.end_time,
            signup_deadline=event.signup_deadline,
            maximum_attendees=event.maximum_attendees,
            status=event.status,
            created_by_discord_id=event.created_by_discord_id,
            created_at=event.created_at,
            updated_at=updated_at,
        )
    async def delete(
        self,
        *,
        guild_id: int,
        event_id: int,
    ) -> bool:
        cursor = await self.database.execute(
            """
            DELETE FROM events
            WHERE guild_id = ?
            AND id = ?
            """,
            (
                guild_id,
                event_id,
            ),
        )

        await self.database.commit()

        return cursor.rowcount > 0