from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


@dataclass
class Event:
    id: int
    guild_id: int
    title: str
    description: str
    location: str
    start_time: datetime
    end_time: datetime | None
    signup_deadline: datetime | None
    maximum_attendees: int | None
    status: EventStatus
    created_by_discord_id: int
    created_at: datetime
    updated_at: datetime