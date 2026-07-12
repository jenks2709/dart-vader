from datetime import datetime
from zoneinfo import ZoneInfo


UK_TIMEZONE = ZoneInfo("Europe/London")


def parse_event_datetime(value: str) -> datetime:
    parsed = datetime.strptime(value.strip(), "%d/%m/%Y %H:%M")
    return parsed.replace(tzinfo=UK_TIMEZONE)