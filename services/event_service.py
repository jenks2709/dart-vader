from datetime import datetime

from models.event import Event, EventStatus
from repositories.event_repository import EventRepository


class InvalidEventError(Exception):
    pass


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    async def list_upcoming_events(
        self,
        *,
        guild_id: int,
        limit: int = 10,
    ) -> list[Event]:
        if limit <= 0:
            raise InvalidEventError(
                "The event limit must be greater than zero."
            )

        return await self.repository.list_upcoming(
            guild_id=guild_id,
            limit=limit,
        )
    async def create_event(
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
        created_by_discord_id: int,
    ) -> Event:
        title = title.strip()
        description = description.strip()
        location = location.strip()

        if not title:
            raise InvalidEventError("The event title cannot be empty.")

        if start_time <= datetime.now(start_time.tzinfo):
            raise InvalidEventError("The event must start in the future.")

        if end_time is not None and end_time <= start_time:
            raise InvalidEventError(
                "The event end time must be after its start time."
            )

        if (
            signup_deadline is not None
            and signup_deadline > start_time
        ):
            raise InvalidEventError(
                "The signup deadline cannot be after the event starts."
            )

        if maximum_attendees is not None and maximum_attendees <= 0:
            raise InvalidEventError(
                "Maximum attendees must be greater than zero."
            )

        return await self.repository.create(
            guild_id=guild_id,
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            signup_deadline=signup_deadline,
            maximum_attendees=maximum_attendees,
            status=EventStatus.SCHEDULED,
            created_by_discord_id=created_by_discord_id,
        )