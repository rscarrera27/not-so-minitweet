from abc import ABC
from app.common.datetime import get_utc_datetime
from datetime import datetime
from uuid import UUID


class Event(ABC):
    occurred_at: datetime


class DomainEvent(Event):
    source_id: UUID
    version: int

    def __post_init__(self):
        self.occurred_at = get_utc_datetime()


class IntegrationEvent(Event):
    source: str
    destination: str
