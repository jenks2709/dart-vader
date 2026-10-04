from dataclasses import dataclass
from datetime import datetime

@dataclass
class Member:
    id: int
    discord_user_id: int
    guild_id: int
    first_name: str
    last_name: str
    display_name: str
    joined_at: datetime
