from datetime import datetime

from models.event import Event, EventStatus
from services.database_service import DatabaseService
from models.event_signup import EventSignup, EventSignupStatus

class EventRepository:
    def __init__(self, database: DatabaseService) -> None:
        self.database = database

    async def withdraw_signup(
        self,
        *,
        guild_id: int,
        event_id: int,
        discord_id: int,
    ) -> bool:
        event = await self.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise ValueError("Event not found.")

        cursor = await self.database.execute(
            """
            SELECT
                id,
                signup_status
            FROM event_signups
            WHERE event_id = ?
            AND discord_id = ?
            LIMIT 1
            """,
            (
                event_id,
                discord_id,
            ),
        )

        signup = await cursor.fetchone()

        if signup is None:
            raise ValueError(
                "You are not signed up for this event."
            )

        if signup["signup_status"] == "cancelled":
            raise ValueError(
                "You have already withdrawn from this event."
            )

        updated_at = datetime.now().astimezone()

        cursor = await self.database.execute(
            """
            UPDATE event_signups
            SET
                signup_status = ?,
                updated_at = ?
            WHERE event_id = ?
            AND discord_id = ?
            """,
            (
                "cancelled",
                updated_at.isoformat(),
                event_id,
                discord_id,
            ),
        )

        await self.database.commit()

        return cursor.rowcount > 0
    async def register_attendance(
        self,
        *,
        guild_id: int,
        event_id: int,
        discord_id: int,
        attended: bool,
    ) -> None:
        event = await self.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise ValueError("Event not found.")

        cursor = await self.database.execute(
            """
            SELECT
                id,
                signup_status
            FROM event_signups
            WHERE event_id = ?
            AND discord_id = ?
            LIMIT 1
            """,
            (
                event_id,
                discord_id,
            ),
        )

        signup = await cursor.fetchone()

        if signup is None:
            raise ValueError(
                "This user is not signed up for the event."
            )

        if signup["signup_status"] == "cancelled":
            raise ValueError(
                "Attendance cannot be registered for a cancelled signup."
            )

        new_status = "attended" if attended else "no_show"
        updated_at = datetime.now().astimezone()

        cursor = await self.database.execute(
            """
            UPDATE event_signups
            SET
                signup_status = ?,
                updated_at = ?
            WHERE event_id = ?
            AND discord_id = ?
            """,
            (
                new_status,
                updated_at.isoformat(),
                event_id,
                discord_id,
            ),
        )

        await self.database.commit()

        if cursor.rowcount == 0:
            raise ValueError("Attendance could not be updated.")
    async def get_signup_counts(
        self,
        *,
        guild_id: int,
        event_id: int,
    ) -> dict[EventSignupStatus, int]:
        event = await self.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise ValueError("Event not found.")

        cursor = await self.database.execute(
            """
            SELECT
                signup_status,
                COUNT(*) AS total
            FROM event_signups
            WHERE event_id = ?
            GROUP BY signup_status
            """,
            (event_id,),
        )

        rows = await cursor.fetchall()

        counts = {
            status: 0
            for status in EventSignupStatus
        }

        for row in rows:
            status = EventSignupStatus(row["signup_status"])
            counts[status] = row["total"]

        return counts

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
    async def sign_up(
        self,
        *,
        guild_id: int,
        event_id: int,
        discord_id: int,
        notes: str | None = None,
    ) -> EventSignup:
        event = await self.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise ValueError("Event not found.")

        if event.status is not EventStatus.SCHEDULED:
            raise ValueError("This event is not accepting signups.")

        now = datetime.now().astimezone()

        if (
            event.signup_deadline is not None
            and now > event.signup_deadline
        ):
            raise ValueError("The signup deadline has passed.")

        cursor = await self.database.execute(
            """
            SELECT
                id,
                signup_status
            FROM event_signups
            WHERE event_id = ?
            AND discord_id = ?
            LIMIT 1
            """,
            (
                event_id,
                discord_id,
            ),
        )

        existing_signup = await cursor.fetchone()

        if (
            existing_signup is not None
            and existing_signup["signup_status"]
            != EventSignupStatus.CANCELLED.value
        ):
            raise ValueError("You are already signed up for this event.")

        cursor = await self.database.execute(
            """
            SELECT COUNT(*) AS attendee_count
            FROM event_signups
            WHERE event_id = ?
            AND signup_status = ?
            """,
            (
                event_id,
                EventSignupStatus.SIGNED_UP.value,
            ),
        )

        count_row = await cursor.fetchone()
        attendee_count = count_row["attendee_count"]

        signup_status = EventSignupStatus.SIGNED_UP

        if (
            event.maximum_attendees is not None
            and attendee_count >= event.maximum_attendees
        ):
            signup_status = EventSignupStatus.WAITLISTED

        timestamp = now.isoformat()

        if existing_signup is not None:
            await self.database.execute(
                """
                UPDATE event_signups
                SET
                    signup_status = ?,
                    signup_time = ?,
                    updated_at = ?,
                    notes = ?
                WHERE event_id = ?
                AND discord_id = ?
                """,
                (
                    signup_status.value,
                    timestamp,
                    timestamp,
                    notes,
                    event_id,
                    discord_id,
                ),
            )
        else:
            await self.database.execute(
                """
                INSERT INTO event_signups (
                    event_id,
                    discord_id,
                    signup_status,
                    signup_time,
                    updated_at,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    discord_id,
                    signup_status.value,
                    timestamp,
                    timestamp,
                    notes,
                ),
            )

        await self.database.commit()

        cursor = await self.database.execute(
            """
            SELECT
                id,
                event_id,
                discord_id,
                signup_status,
                signup_time,
                updated_at,
                notes
            FROM event_signups
            WHERE event_id = ?
            AND discord_id = ?
            LIMIT 1
            """,
            (
                event_id,
                discord_id,
            ),
        )

        row = await cursor.fetchone()

        if row is None:
            raise RuntimeError("Failed to retrieve signup after creation.")

        return EventSignup(
            id=row["id"],
            event_id=row["event_id"],
            discord_id=row["discord_id"],
            status=EventSignupStatus(row["signup_status"]),
            signup_time=datetime.fromisoformat(row["signup_time"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            notes=row["notes"],
        )
    async def list_signups(
        self,
        *,
        guild_id: int,
        event_id: int,
        include_cancelled: bool = False,
    ) -> list[EventSignup]:
        event = await self.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise ValueError("Event not found.")

        if include_cancelled:
            query = """
                SELECT
                    id,
                    event_id,
                    discord_id,
                    signup_status,
                    signup_time,
                    updated_at,
                    notes
                FROM event_signups
                WHERE event_id = ?
                ORDER BY
                    CASE signup_status
                        WHEN 'signed_up' THEN 1
                        WHEN 'waitlisted' THEN 2
                        WHEN 'attended' THEN 3
                        WHEN 'no_show' THEN 4
                        WHEN 'cancelled' THEN 5
                        ELSE 6
                    END,
                    signup_time ASC
            """

            parameters = (event_id,)

        else:
            query = """
                SELECT
                    id,
                    event_id,
                    discord_id,
                    signup_status,
                    signup_time,
                    updated_at,
                    notes
                FROM event_signups
                WHERE event_id = ?
                AND signup_status != ?
                ORDER BY
                    CASE signup_status
                        WHEN 'signed_up' THEN 1
                        WHEN 'waitlisted' THEN 2
                        WHEN 'attended' THEN 3
                        WHEN 'no_show' THEN 4
                        ELSE 5
                    END,
                    signup_time ASC
            """

            parameters = (
                event_id,
                EventSignupStatus.CANCELLED.value,
            )

        cursor = await self.database.execute(
            query,
            parameters,
        )

        rows = await cursor.fetchall()

        return [
            EventSignup(
                id=row["id"],
                event_id=row["event_id"],
                discord_id=row["discord_id"],
                status=EventSignupStatus(row["signup_status"]),
                signup_time=datetime.fromisoformat(row["signup_time"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                notes=row["notes"],
            )
            for row in rows
        ]