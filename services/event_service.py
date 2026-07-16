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
    async def get_event(
        self,
        *,
        guild_id: int,
        event_id: int,
    ) -> Event:
        if event_id <= 0:
            raise InvalidEventError(
                "The event ID must be greater than zero."
            )

        event = await self.repository.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise InvalidEventError(
                f"No event was found with ID {event_id}."
            )

        return event
    async def edit_event(
        self,
        *,
        guild_id: int,
        event_id: int,
        title: str | None = None,
        description: str | None = None,
        location: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        signup_deadline: datetime | None = None,
        maximum_attendees: int | None = None,
    ) -> Event:
        if event_id <= 0:
            raise InvalidEventError(
                "The event ID must be greater than zero."
            )

        event = await self.repository.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise InvalidEventError(
                f"No event was found with ID {event_id}."
            )

        updated_title = event.title
        updated_description = event.description
        updated_location = event.location
        updated_start_time = event.start_time
        updated_end_time = event.end_time
        updated_signup_deadline = event.signup_deadline
        updated_maximum_attendees = event.maximum_attendees

        if title is not None:
            title = title.strip()

            if not title:
                raise InvalidEventError(
                    "The event title cannot be empty."
                )

            updated_title = title

        if description is not None:
            updated_description = description.strip()

        if location is not None:
            location = location.strip()

            if not location:
                raise InvalidEventError(
                    "The event location cannot be empty."
                )

            updated_location = location

        if start_time is not None:
            updated_start_time = start_time

        if end_time is not None:
            updated_end_time = end_time

        if signup_deadline is not None:
            updated_signup_deadline = signup_deadline

        if maximum_attendees is not None:
            if maximum_attendees <= 0:
                raise InvalidEventError(
                    "Maximum attendees must be greater than zero."
                )

            updated_maximum_attendees = maximum_attendees

        if updated_start_time <= datetime.now(
            updated_start_time.tzinfo
        ):
            raise InvalidEventError(
                "The event must start in the future."
            )

        if (
            updated_end_time is not None
            and updated_end_time <= updated_start_time
        ):
            raise InvalidEventError(
                "The event end time must be after its start time."
            )

        if (
            updated_signup_deadline is not None
            and updated_signup_deadline > updated_start_time
        ):
            raise InvalidEventError(
                "The signup deadline cannot be after the event starts."
            )

        updated_event = Event(
            id=event.id,
            guild_id=event.guild_id,
            title=updated_title,
            description=updated_description,
            location=updated_location,
            start_time=updated_start_time,
            end_time=updated_end_time,
            signup_deadline=updated_signup_deadline,
            maximum_attendees=updated_maximum_attendees,
            status=event.status,
            created_by_discord_id=event.created_by_discord_id,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )

        return await self.repository.update(
            event=updated_event,
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
    async def delete_event(
        self,
        *,
        guild_id: int,
        event_id: int,
    ) -> Event:
        if event_id <= 0:
            raise InvalidEventError(
                "The event ID must be greater than zero."
            )

        event = await self.repository.get_by_id(
            guild_id=guild_id,
            event_id=event_id,
        )

        if event is None:
            raise InvalidEventError(
                f"No event was found with ID {event_id}."
            )

        deleted = await self.repository.delete(
            guild_id=guild_id,
            event_id=event_id,
        )

        if not deleted:
            raise InvalidEventError(
                "The event could not be deleted."
            )

        return event