<<<<<<< HEAD
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventSignupStatus(Enum):
    SIGNED_UP = "signed_up"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"
    ATTENDED = "attended"
    NO_SHOW = "no_show"


@dataclass
class EventSignup:
    event_id: str
    discord_id: int
    status: EventSignupStatus
    signup_time: datetime
    updated_at: datetime
    notes: str | None = None

@dataclass
class EventSignupWithMember:
    discord_id: int
    status: EventSignupStatus
    signup_time: datetime
    notes: str | None = None
    first_name: str | None = None
    last_name: str | None = None
=======
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventSignupStatus(Enum):
    SIGNED_UP = "signed_up"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"
    ATTENDED = "attended"
    NO_SHOW = "no_show"


@dataclass
class EventSignup:
    event_id: str
    discord_id: int
    status: EventSignupStatus
    signup_time: datetime
    updated_at: datetime
    notes: str | None = None

@dataclass
class EventSignupWithMember:
    discord_id: int
    status: EventSignupStatus
    signup_time: datetime
    notes: str | None = None
    first_name: str | None = None
    last_name: str | None = None
>>>>>>> 70ee258 (Connecting traspberry pi and fix minor version compatability issues)
    display_name: str | None = None